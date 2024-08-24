from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from user_statistics.models import Statistics
from user_statistics.serializers import StatisticsUpdateSerializer
from authorization.models import DwUser
from user_statistics.serializers import UserDetailSerializer


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
