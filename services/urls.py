from django.urls import path
from . import views

urlpatterns = [
    path("", views.services_dashboard, name="services"),
    # Original PoP endpoint
    path("pop/<int:service_id>/", views.pop_info, name="pop_info"),
    # New explicit API endpoint
    path(
        "api/pop-detail/<int:service_id>/",
        views.pop_detail_api,
        name="pop_detail_api",
    ),
]
