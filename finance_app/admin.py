from django.contrib import admin
from finance_app.models import Wallet, Expense

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Expense)
