from rest_framework import serializers
from .models import Investment
from django.db import models
from finance_app.models import Wallet
from rest_framework.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
import yfinance as yf


class InvestmentSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    date = serializers.DateField(required=False)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Investment
        fields = "__all__"
        read_only_fields = ["user", "current_price"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remove SIP fields if asset_type is 'stock'
        if instance.asset_type == "stock":
            data.pop("sip_start_date", None)
            data.pop("sip_frequency", None)
            data.pop("sip_end_date", None)

        # If is_manual is False, hide price from frontend
        if not instance.is_manual:
            data.pop("price", None)

        return data

    def validate(self, attrs):
        is_manual = attrs.get(
            "is_manual", self.instance.is_manual if self.instance else None
        )

        if is_manual:
            if attrs.get("price") is None:
                raise ValidationError(
                    {"price": "Price is required when is_manual is True."}
                )
            if attrs.get("date") is None:
                raise ValidationError(
                    {"date": "Date is required when is_manual is True."}
                )
        else:
            if "price" in attrs:
                raise ValidationError(
                    {"price": "Price should not be provided when is_manual is False."}
                )
            if "date" in attrs:
                raise ValidationError(
                    {"date": "Date should not be provided when is_manual is False."}
                )

        return attrs

    def get_total_amount(self, obj):
        return float(
            (Decimal(str(obj.quantity)) * Decimal(str(obj.current_price))).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        )

    def get_live_price(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            price = stock.info.get("regularMarketPrice", None)
            if price is not None:
                return Decimal(str(price))
            raise ValueError(f"No price found for {symbol}")
        except Exception as e:
            raise ValidationError(
                {"detail": f"Failed to fetch price for {symbol}: {str(e)}"}
            )

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        validated_data["user"] = user

        wallet, _ = Wallet.objects.get_or_create(user=user)
        transaction_type = validated_data["transaction_type"]
        quantity = validated_data["quantity"]
        symbol = validated_data["symbol"]

        if transaction_type == "buy":
            if validated_data.get("is_manual", False):
                price = validated_data["price"]
                amount = Decimal(str(quantity * price))
            else:
                # Fetch live price
                price = self.get_live_price(symbol)
                validated_data["price"] = price
                validated_data["date"] = date.today()
                validated_data["current_price"] = price
                amount = Decimal(str(quantity)) * price

            # Balance update for buying
            if wallet.balance < amount:
                raise ValidationError({"detail": "Insufficient wallet balance to buy."})
            wallet.balance -= amount

            # Save investment
            wallet.save()
            return super().create(validated_data)
        else:
            raise ValidationError(
                {"detail": "Only buy transactions can be created here."}
            )

    def update(self, instance, validated_data):
        wallet, _ = Wallet.objects.get_or_create(user=instance.user)

        # Revert old transaction if updating an existing record
        old_amount = Decimal(str(instance.quantity)) * Decimal(str(instance.price))

        if instance.transaction_type == "buy":
            wallet.balance += old_amount
        elif instance.transaction_type == "sell":
            wallet.balance -= old_amount

        # Prepare new transaction details
        new_quantity = validated_data.get("quantity", instance.quantity)
        new_price = validated_data.get("price", instance.price)
        new_transaction_type = validated_data.get(
            "transaction_type", instance.transaction_type
        )
        new_amount = Decimal(str(new_quantity)) * Decimal(str(new_price))

        if new_transaction_type == "buy":
            # Ensure sufficient wallet balance for buy transaction
            if wallet.balance < new_amount:
                raise ValidationError(
                    {"detail": "Insufficient wallet balance to update this buy."}
                )
            wallet.balance -= new_amount
        elif new_transaction_type == "sell":
            # Ensure the user owns enough stocks to sell
            owned_quantity = (
                Investment.objects.filter(
                    user=instance.user, asset_type="stock", symbol=instance.symbol
                ).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"]
                or 0
            )

            if owned_quantity < new_quantity:
                raise ValidationError(
                    {"detail": f"Insufficient stock of {instance.symbol} to sell."}
                )

            # Decrease the quantity of stocks the user owns
            investment = Investment.objects.filter(
                user=instance.user, asset_type="stock", symbol=instance.symbol
            ).first()

            if investment:
                investment.quantity -= new_quantity
                investment.save()

            # Update wallet balance for sell transaction
            wallet.balance += new_amount

        # Save changes to wallet
        wallet.save()
        return super().update(instance, validated_data)
