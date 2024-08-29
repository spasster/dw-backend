from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse

from user_statistics.models import Statistics
from user_statistics.serializers import StatisticsUpdateSerializer
from authorization.models import DwUser
from user_statistics.serializers import UserPrivateDetailSerializer, UserPublicDetailSerializer
from user_statistics.models import RefferalSystem


class AddPlaytime(generics.UpdateAPIView):
    """Обновление статистики"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Statistics.objects.all()
    serializer_class = StatisticsUpdateSerializer

    def get_user_statistics(self, user):
        try:
            return Statistics.objects.get(user=user)
        except Statistics.DoesNotExist:
            raise NotFound('Statistics not found for this user.')
    
    def patch(self, request):
        """Можно прокидывать только определенные поля блягодаря partial=True"""

        user = request.user
        statistics = self.get_user_statistics(user)

        serializer = StatisticsUpdateSerializer(statistics, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateRefferals(APIView):
    """Открытие реферальной системы юзеру"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    
    def patch(self, request):
        user = request.user
        code = request.data.get('code')

        if not code:
            return Response({"error": "Referral code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refferal_system = RefferalSystem.objects.get(user=user)
            refferal_system.activate_refferal_system(code)
            return Response({"message": "Referral system enabled successfully."}, status=status.HTTP_200_OK)
        except RefferalSystem.DoesNotExist:
            return Response({"error": "Refferal system not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
class GetPrivateInfo(generics.RetrieveAPIView):
    """Получение текущего аутентифицированного пользователя"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = DwUser.objects.all()
    serializer_class = UserPrivateDetailSerializer

    def get_object(self):
        user = get_object_or_404(DwUser, id=self.request.user.id)
        return user

        
class GetPublickInfo(generics.RetrieveAPIView):
    """Получение юзера по нику"""

    serializer_class = UserPublicDetailSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(DwUser, username=username)
        return user
    
    
class CheckRefferal(View):
    """Проверка что такое рефферал код есть"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        code = request.GET.get('code', None)
        
        if code is None:
            return JsonResponse({'error': 'No referral code provided'}, status=400)

        # Проверка, существует ли код
        exists = RefferalSystem.objects.filter(code=code).exists()

        if exists:
            return JsonResponse({'exists': True}, status=200)
        else:
            return JsonResponse({'exists': False}, status=404)