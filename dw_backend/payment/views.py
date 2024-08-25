from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from user_statistics.models import RefferalSystem

class MakePayment(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]
    
    def AddRefferalNumber(refferal_code):
        refferal_system = get_object_or_404(RefferalSystem, code=refferal_code)
        refferal_system.refferal_number = (refferal_system.refferal_number or 0) + 1
        refferal_system.save()

    def post(self, request, *args, **kwargs):
        refferal_code = request.data.get('code')
        user = request.user
        
        if not refferal_code:
            pass

        if refferal_code:
            self.AddRefferalNumber(refferal_code)
            return Response({"message": "Refferal code applied successfully."}, status=status.HTTP_200_OK)
