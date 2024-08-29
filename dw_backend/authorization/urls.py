from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
import authorization.views as views

urlpatterns = [
    path('register/', views.RegistrationViewSet.as_view({'post': 'create_user'}), name='auth_register'),
    path('login/', views.CustomAuth.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('set_hwid/', views.SetHWIDView.as_view(), name='auth_hwid'),
    path('change_password/', views.ChangePasswordView.as_view(), name='auth_change'),
]
