from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny

from base64 import b64decode
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, tokens

from .serializers import EmailSerializer, MyTokenObtainPairSerializer, RegisterSerializer, UserInterestSerializer

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    """
    login by sending a post request containing username and password to login/
    """
    
    serializer_class = MyTokenObtainPairSerializer
    my_tags = ["Authentication"]


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "success", "message": serializer.errors}, status=status.HTTP_201_CREATED)
      

class UserInterestView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserInterestSerializer(context={'user': request.user}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'interest saved successfully'})
        else:
            return Response({'status': 'error', 'errors': serializer.errors})



class ResendMail(APIView):
    """
    Resend Verification Email 

    """
    
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'message': "Check Email For Verification"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': "Invalid Request"
            }, status=status.HTTP_400_BAD_REQUEST)
        


class VerifyAccount(APIView):

    """
    Allows Users To be activated after registration , by clicking link sent to their mail . This is used for email verification.
    Returns Interest endpoint to continue 
    """
    my_tags = ["Authentication"]

    def get(self, request, uidb64, token):
        try:
            uid = int(b64decode(uidb64).decode('utf8'))
            user = User.objects.get(pk=uid)
            if not tokens.default_token_generator.check_token(user, token):
                raise Exception
            user.is_active = True
            user.email_confirmed = True
            user.save(update_fields=['email_confirmed', 'is_active'])
            return redirect(f'https://c-novels-frontend.vercel.app/verify-success/{uid}')

        except :
            return redirect(f'https://c-novels-frontend.vercel.app/verify-failure/{uid}')