from django.urls import path
from payment import views

urlpatterns = [
    path('make_payment/', views.MakePayment.as_view(), name='make_payment'),
]
