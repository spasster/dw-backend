from django.urls import path
from user_statistics import views

urlpatterns = [
    path('stat/', views.AddPlaytime.as_view(), name='add_stat'),
]
