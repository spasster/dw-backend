from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from user_statistics.models import Statistics
from user_statistics.serializers import StatisticsUpdateSerializer
from authorization.models import DwUser
from user_statistics.serializers import UserDetailSerializer
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

class GetViewSet(generics.RetrieveAPIView):
    """Получение юзера по нику"""

    queryset = DwUser.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self ):
        username = self.request.data['username']
        try:
            return DwUser.objects.get(username=username)
        except DwUser.DoesNotExist:
            raise NotFound('User not found')
