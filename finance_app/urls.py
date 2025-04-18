from django.urls import path
from .views import (
    ExpenseListCreateAPIView,
    ExpenseUpdateAPIView,
    ExpensePartialUpdateAPIView,
    WalletCreateAPIView,
)

urlpatterns = [
    path("expenses/", ExpenseListCreateAPIView.as_view(), name="expense-list-create"),
    path("expenses/<int:pk>/", ExpenseUpdateAPIView.as_view(), name="expense-update"),
    path(
        "expenses/<int:pk>/partial/",
        ExpensePartialUpdateAPIView.as_view(),
        name="expense-partial-update",
    ),
    path("wallet/", WalletCreateAPIView.as_view(), name="wallet-detail"),
]
