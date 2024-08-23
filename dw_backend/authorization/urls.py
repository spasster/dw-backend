from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
import authorization.views as views

urlpatterns = [
    path('register/', views.RegistrationViewSet.as_view({'post': 'post'}), name='auth_register'),
    path('getUsers/', views.GetViewSet.as_view({'get': 'list'}), name='auth_get'),
    path('login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]
