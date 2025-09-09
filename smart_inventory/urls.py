from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="products:product_list", permanent=False)),
    path("products/", include("products.urls", namespace="products")),
    path("billing/", include("billing.urls", namespace="billing")),
    # optionally add customers urls if you made them
    path("accounts/", include("django.contrib.auth.urls")),
]
