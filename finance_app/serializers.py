from rest_framework import serializers
from .models import Wallet, Expense, Income
from rest_framework.exceptions import ValidationError


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "category",
            "subcategory",
            "payment_method",
            "description",
            "date",
        ]
        read_only_fields = ["id", "date"]

    def create(self, validated_data):
        user = self.context["request"].user
        wallet = Wallet.objects.get(user=user)
        expense_amount = validated_data["amount"]

        if wallet.balance < expense_amount:
            raise ValidationError({"detail": "Insufficient balance."})

        expense = Expense.objects.create(user=user, **validated_data)

        # Deduct amount from wallet
        wallet.balance -= expense.amount
        wallet.save()

        return expense


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "amount",
            "category",
            "description",
            "date",
        ]
        read_only_fields = ["id", "date"]

    def create(self, validated_data):
        user = self.context["request"].user
        wallet, _ = Wallet.objects.get_or_create(user=user)

        income = Income.objects.create(user=user, **validated_data)

        # Add amount to wallet
        wallet.balance += income.amount
        wallet.save()

        return income

    def update(self, instance, validated_data):
        user = self.context["request"].user
        wallet, _ = Wallet.objects.get_or_create(user=user)

        old_amount = instance.amount
        new_amount = validated_data.get("amount", old_amount)

        instance = super().update(instance, validated_data)

        # Adjust wallet balance if income amount changes
        wallet.balance += new_amount - old_amount
        wallet.save()

        return instance
