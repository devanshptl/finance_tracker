from django.contrib import admin
from finance_app.models import Wallet, Expense, Income

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Expense)
admin.site.register(Income)
