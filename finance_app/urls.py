from django.urls import path
from .views import (
    ExpenseAPIView,
    WalletCreateAPIView,
    IncomeAPIView,
)

urlpatterns = [
    path("expenses/", ExpenseAPIView.as_view(), name="expense-list-create"),
    path("expenses/<int:pk>/", ExpenseAPIView.as_view(), name="expense-detail"),
    path("wallet/", WalletCreateAPIView.as_view(), name="wallet-detail"),
    path("incomes/", IncomeAPIView.as_view(), name="income-list-create"),
    path("incomes/<int:pk>/", IncomeAPIView.as_view(), name="income-detail"),
]
