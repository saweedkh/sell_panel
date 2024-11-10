# Django Built-in modules
from django.urls import path

# Local Apps
from . import views

# Third Party Packages
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account'

urlpatterns = [
        path('otp/send/', views.SendOtpView.as_view(), name='otp_send'),
        path('otp/verify/', views.OtpVerifyView.as_view(), name='otp_verify'),
        path('register/', views.RegisterView.as_view(), name='register'),
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('profile/', views.ProfileView.as_view(), name='profile'),
        # path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
        path('update-profile/', views.UpdateProfileView.as_view(), name='update_profile'),
        # path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
        path('transaction/', views.TransactionView.as_view(), name='transaction'),

    path('addresses/', views.UserAddressListView.as_view(), name='user_addresses'),
    path('addresses/edit/<pk>', views.UserAddressRetrieveUpdateDestroyView.as_view(), name='user_addresses_edit'),
    
    
    
    
    
]
