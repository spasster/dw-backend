from django.urls import path
from subscription import views

urlpatterns = [
    path('activate_key/', views.KeyActivationsView.as_view(), name='activate_key'),
    path('new_keys/', views.NewKeys.as_view(), name='new_keys'),
]
