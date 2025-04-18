from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User


class Investment(models.Model):
    ASSET_TYPES = [
        ("stock", "Stock"),
        ("mutual_fund", "Mutual Fund"),
        ("sip", "SIP"),
    ]

    TRANSACTION_TYPES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)

    quantity = models.FloatField()
    price = models.FloatField()
    date = models.DateField()

    current_price = models.FloatField(null=True, blank=True)
    is_manual = models.BooleanField(default=False)

    # Optional fields for SIPs
    sip_start_date = models.DateField(null=True, blank=True)
    sip_frequency = models.CharField(max_length=20, null=True, blank=True)
    sip_end_date = models.DateField(null=True, blank=True)

    def total_invested(self):
        return self.quantity * self.price if self.transaction_type == "buy" else 0

    def current_value(self):
        return self.quantity * (self.current_price or self.price)

    def returns_absolute(self):
        return self.current_value() - self.total_invested()

    def returns_percentage(self):
        invested = self.total_invested()
        return (self.returns_absolute() / invested) * 100 if invested else 0

    def __str__(self):
        return f"{self.user.username} - {self.asset_type} - {self.symbol} - {self.transaction_type}"
