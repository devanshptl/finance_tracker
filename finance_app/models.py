from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from portfolio.models import Investment
from decimal import Decimal


# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    @property
    def asset(self):
        total_asset_value = Investment.objects.filter(
            user=self.user, transaction_type="buy"
        ).aggregate(total=models.Sum(models.F("quantity") * models.F("price")))[
            "total"
        ] or Decimal(
            0
        )
        return total_asset_value

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - Expense"


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - Income"
