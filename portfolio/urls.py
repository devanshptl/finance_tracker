from django.urls import path
from .views import BuyInvestmentAPIView, SellInvestmentAPIView

urlpatterns = [
    path(
        "investments/buy/", BuyInvestmentAPIView.as_view(), name="buy-investment-list"
    ),
    path(
        "investments/sell/",
        SellInvestmentAPIView.as_view(),
        name="sell-investment-list",
    ),
    path(
        "investments/buy/<int:pk>/",
        BuyInvestmentAPIView.as_view(),
        name="buy-investment-detail",
    ),
    path(
        "investments/sell/<int:pk>/",
        SellInvestmentAPIView.as_view(),
        name="sell-investment-detail",
    ),
]
