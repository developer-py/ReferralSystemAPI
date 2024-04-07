from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer,UserDetailsSerializer,UserLoginSerialiazer
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
class UserRegistrationAPIView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'user_id': user.id,
                'message': 'User registration successfully'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailsSerializer

class AllUsersAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailsSerializer

    
    
    
class UserLoginView(APIView):
    def post(self,request,format=None):
        serialiazer=UserLoginSerialiazer(data=request.data)
        if serialiazer.is_valid(raise_exception=True):                                                                                                                                                                                                                                                                                              
            email=serialiazer.data.get('email')
            password=serialiazer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:    
                token=get_tokens_for_user(user)
                
                return Response({'user_id': user.id,'token':token, 'msg':"Login Success","status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        return Response(serialiazer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
class ReferralsAPIView(generics.ListAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2 

    def get_queryset(self):
        user = self.request.user
        if user.referral_code:
            return CustomUser.objects.filter(referred_by=user)
        else:
            return CustomUser.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

