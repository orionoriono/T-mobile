from django.urls import path
from . import views

urlpatterns = [
    path("deploy/", views.deploy_service, name="deploy_service"),
]
