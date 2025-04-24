from django.urls import path
from .views import (
    ExpenseAPIView,
    WalletCreateAPIView,
    IncomeAPIView,
    MonthlySummaryAPIView,
    MonthlyReportEmailAPIView,
)

urlpatterns = [
    path("expenses/", ExpenseAPIView.as_view(), name="expense-list-create"),
    path("expenses/<int:pk>/", ExpenseAPIView.as_view(), name="expense-detail"),
    path("wallet/", WalletCreateAPIView.as_view(), name="wallet-detail"),
    path("incomes/", IncomeAPIView.as_view(), name="income-list-create"),
    path("incomes/<int:pk>/", IncomeAPIView.as_view(), name="income-detail"),
    path("summary/", MonthlySummaryAPIView.as_view(), name="monthly-summary"),
    path(
        "send_monthly_report/",
        MonthlyReportEmailAPIView.as_view(),
        name="send_monthly_report",
    ),
]
