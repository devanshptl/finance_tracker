from celery import shared_task
from .models import Investment
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from decimal import Decimal


@shared_task
def execute_sip():
    active_sips = Investment.objects.filter(
        asset_type="sip", is_sip_active=True, next_sip_date__lte=timezone.now()
    )

    for investment in active_sips:
        # Check if the current date matches the next SIP execution date
        if (
            investment.sip_end_date
            and investment.next_sip_date > investment.sip_end_date
        ):
            continue

        current_price = Decimal(investment.current_price or investment.price)

        wallet = investment.user.wallet
        total_amount = current_price * Decimal(investment.quantity)

        if wallet.balance >= total_amount:
            wallet.balance -= total_amount
            wallet.save()

            investment.transaction_type = "buy"
            investment.save()

            # Send email notification to the user
            send_mail(
                "SIP Execution Successful",
                f"Your SIP for {investment.name} has been successfully executed for {investment.quantity} units.",
                settings.DEFAULT_FROM_EMAIL,
                [investment.user.email],
            )

            # Update next SIP date based on frequency
            if investment.sip_frequency == "daily":
                investment.next_sip_date += timedelta(days=1)
            elif investment.sip_frequency == "weekly":
                investment.next_sip_date += timedelta(weeks=1)
            elif investment.sip_frequency == "monthly":
                next_month = investment.next_sip_date.month % 12 + 1
                year_increment = investment.next_sip_date.month // 12
                investment.next_sip_date = investment.next_sip_date.replace(
                    year=investment.next_sip_date.year + year_increment,
                    month=next_month,
                )

            investment.save()

        else:
            # Insufficient funds
            send_mail(
                "SIP Execution Failed",
                f"Your SIP for {investment.name} could not be executed due to insufficient balance.",
                settings.DEFAULT_FROM_EMAIL,
                [investment.user.email],
            )
