from django.urls import path
from user_statistics import views

urlpatterns = [
    path('add_stat/', views.AddPlaytime.as_view(), name='add_stat'),
    path('get_user/', views.GetViewSet.as_view(), name='user_get'),
    path('activate_ref/', views.ActivateRefferals.as_view(), name='activate_ref'),
]
