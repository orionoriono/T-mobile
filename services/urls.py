from django.urls import path
from . import views

urlpatterns = [
    path("", views.services_dashboard, name="services"),
    # Original PoP endpoint
    path("api/details/<int:service_id>/", views.details_detail_api, name="details_detail_api"),
]
