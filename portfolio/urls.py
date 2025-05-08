from django.urls import path
from .views import (
    BuyInvestmentAPIView,
    SellInvestmentAPIView,
    StartSIPAPIView,
    StopSIPAPIView,
    PortfolioAnalyticsView,
)

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
    path(
        "investments/sip/start/",
        StartSIPAPIView.as_view(),
        name="start-sip",
    ),
    path(
        "investments/sip/stop/",
        StopSIPAPIView.as_view(),
        name="stop-sip",
    ),
    path(
        "investments/sip/start/<int:investment_id>/",
        StartSIPAPIView.as_view(),
        name="start-sip-detail",
    ),
    path(
        "investments/sip/stop/<int:investment_id>/",
        StopSIPAPIView.as_view(),
        name="stop-sip-detail",
    ),
    path("analytics/", PortfolioAnalyticsView.as_view(), name="portfolio-analytics"),
]
