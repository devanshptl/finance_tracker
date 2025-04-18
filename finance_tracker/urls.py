from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("finance/", include("finance_app.urls")),
    path("portfolio/", include("portfolio.urls")),
]
