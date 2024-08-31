from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from subscription.models import SubscriptionKey

class KeyActivationsView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        key = request.data.get('key')
        user = request.user

        if not key:
            return JsonResponse({'error': 'No key provided'}, status=400)

        try:
            SubscriptionKey.objects.activate_sub_key(key=key, user=user)
            return JsonResponse({'message': 'Key activated!'}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

class NewKeys(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        # key_number = request.data.get('number')
        # user = request.user

        try:
            # SubscriptionKey.objects.activate_sub_key(key=key, user=user)
            return JsonResponse({'message': 'Key activated!'}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)