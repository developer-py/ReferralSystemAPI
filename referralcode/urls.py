# users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/', AllUsersAPIView.as_view(), name='all-users'),  
    path('login/', UserLoginView.as_view(), name='users-login'),  
    path('referrals/', ReferralsAPIView.as_view(), name='referrals-list'),

    
]
