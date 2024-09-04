from django.urls import path
from user_statistics import views

urlpatterns = [
    path('add_stat/', views.AddPlaytime.as_view(), name='add_stat'),

    path('get_user/<str:username>/', views.GetPublickInfo.as_view(), name='public_user_get'),
    path('get_myself/', views.GetPrivateInfo.as_view(), name='private_user_get'),

    path('activate_ref/', views.ActivateRefferals.as_view(), name='activate_ref'),
    path('check_ref/', views.CheckRefferal.as_view(), name='check_ref'),
]
