from rest_framework.response import Response
from rest_framework import status, generics
# from rest_framework.authtoken.models import Token
# from ..serializers.user import UserSerializer
# from django.contrib.auth import authenticate, login, logout

class SignUp(generics.CreateAPIView):
    # Override the authentication/permissions classes so this endpoint
    # is not authenticated & we don't need any permissions to access it.
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request):
         print('wahooo')
         return Response({})