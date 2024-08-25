from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user_statistics.models import RefferalSystem
from subscription.models import Subscription

class MakePayment(APIView):
    """создание и отправка плавтежа, потом другой метод слушает как успешно или нет"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def MakePayment():
        """Создание объекта платежа"""
        pass

    def get(self, request, *args, **kwargs):
        sub_dur = request.data.get('type')
        user = request.user

        self.MakePayment()

        
class PaymentSuccess(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def AddRefferalNumber(self, refferal_code):
        """Добавление числа рефералов челу"""
        refferal_system = get_object_or_404(RefferalSystem, code=refferal_code)
        refferal_system.refferal_number = (refferal_system.refferal_number or 0) + 1
        refferal_system.save()

    def AddSubscription(self, sub_dur, user):
        """Добавление подписки юзеру"""
        user_sub = Subscription.objects.get(user = user)
        user_sub.add_subscription(sub_dur)

    def post(self, request, *args, **kwargs):
        refferal_code = request.data.get('code')
        sub_dur = request.data.get('sub_dur')
        user = request.user

        if refferal_code:
            self.AddSubscription(sub_dur, user)
            self.AddRefferalNumber(refferal_code)
            return Response({"message": "Subscription updated successfully."}, status=status.HTTP_200_OK)


        self.AddSubscription(sub_dur, user)
        return Response({"message": "Subscription updated successfully."}, status=status.HTTP_200_OK)


