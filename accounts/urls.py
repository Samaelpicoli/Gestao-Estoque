from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.AccountLoginView.as_view(), name='login'),
]
