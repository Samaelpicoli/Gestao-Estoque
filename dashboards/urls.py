from django.urls import path

from dashboards import views

urlpatterns = [
    path('', views.home, name='home'),
]
