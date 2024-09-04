from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authorization.urls')),
    path('api/v1/sub/', include('subscription.urls')),
    path('api/v1/stat/', include('user_statistics.urls')),
    path('api/v1/payment/', include('payment.urls')),
]
