from django.contrib import admin
from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserProfileView, UserLogoutView

urlpatterns = [
    path('signup', UserRegisterView.as_view(), name='signup'),
    path('signin', UserLoginView.as_view(), name='signin'),
    path('me', UserProfileView.as_view(), name='me'),
    path('logout', UserLogoutView.as_view(), name='logout')
]