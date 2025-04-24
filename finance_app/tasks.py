# your_app/tasks.py
import base64
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
from django.contrib.auth.models import User


@shared_task
def send_report_to_email_async(user_id, pdf_base64):
    pdf_data = base64.b64decode(pdf_base64)
    pdf_buffer = BytesIO(pdf_data)

    user = User.objects.get(id=user_id)

    email = EmailMessage(
        subject="Your Monthly Finance Report",
        body="Hi, please find attached your monthly income/expense summary and charts.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach("Finance_Report.pdf", pdf_buffer.read(), "application/pdf")
    email.send()
