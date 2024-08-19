from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
import authorization.views as views

urlpatterns = [
    path('register/', views.RegistrationViewSet.as_view({'get': 'list'}), name='auth_register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('refresh/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', TokenObtainPairView.as_view(), name='auth_login'),
]
