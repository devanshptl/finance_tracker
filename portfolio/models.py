from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


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

    SIP_FREQUENCIES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
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

    # SIP fields
    sip_start_date = models.DateField(null=True, blank=True)
    sip_frequency = models.CharField(
        max_length=20, choices=SIP_FREQUENCIES, null=True, blank=True
    )
    sip_end_date = models.DateField(null=True, blank=True)
    is_sip_active = models.BooleanField(default=False)
    next_sip_date = models.DateField(null=True, blank=True)  # Track next execution

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

    def initialize_sip(self):
        """Initialize SIP next date when created."""
        if self.asset_type == "sip" and self.sip_start_date:
            self.is_sip_active = True
            self.next_sip_date = self.sip_start_date
            self.save()

    def update_next_sip_date(self):
        """Update the next_sip_date based on frequency after each execution."""
        if self.sip_frequency == "daily":
            self.next_sip_date += timedelta(days=1)
        elif self.sip_frequency == "weekly":
            self.next_sip_date += timedelta(weeks=1)
        elif self.sip_frequency == "monthly":
            next_month = self.next_sip_date.month % 12 + 1
            year_increment = self.next_sip_date.month // 12
            self.next_sip_date = self.next_sip_date.replace(
                year=self.next_sip_date.year + year_increment, month=next_month
            )
        self.save()
