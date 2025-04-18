from rest_framework import serializers
from .models import Wallet, Expense
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
