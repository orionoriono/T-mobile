from django.urls import path
from . import views

urlpatterns = [
    path("", views.services_dashboard, name="services"),
    path("pop/<int:service_id>/", views.pop_info, name="pop_info"),
]
