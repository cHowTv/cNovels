from base64 import b64decode
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InterestSerializers, MyTokenObtainPairSerializer, UserSerializer
from django.contrib.auth import get_user_model, tokens
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

# Create your views here.
class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data":serializer.data}, 
                            status=status.HTTP_201_CREATED)
        return Response({"status": "failed", "data":serializer.errors},
                         status=status.HTTP_400_BAD_REQUEST)


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
            user.save()
            return redirect(f'https://c-novels-frontend.vercel.app/verify-success/{uid}')

        except :
            return redirect(f'https://c-novels-frontend.vercel.app/verify-failure/{uid}')



class UserInterestView(APIView):
    """
    Allows Users to Add interest by using the post request,
     you can also get users' interests by sending a get request
    """
    permission_classes = (permissions.IsAuthenticated,)
    my_tags = ["Authentication"]
    
    def post(self, request):
        # pass request to verify if user already posted
        try:
            serializer = InterestSerializers(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                user = request.user
                serializer.save(user=user)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"status": "failed", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MyTokenObtainPairView(TokenObtainPairView):
    """
    login by sending a post request containing username and password to login/


    """
    
    serializer_class = MyTokenObtainPairSerializer
    my_tags = ["Authentication"]
