from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ArticleSerializer
from .permissions import RolePermission
from .models import Article

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password = password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user' : user_serializer.data
            })
        else:
            return Response({'detail':'Invalid credentials'}, status=401)
            

# class DashboadView(APIView):
#     permission_classes = [IsAuthenticated,HasRole]
#     required_role = 'student'
    
#     def get(self, request):
#         user = request.user
#         user_serializer = UserSerializer(user)
#         return Response({
#             'message': 'Welcome to dashboard',
#             'user' : user_serializer.data
#         }, 200)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]
    required_role = 'student'  # Minimum role to access

    def get(self, request):
        return Response({
            'message': 'Welcome to the dashboard!',
            'user': request.user.username
        })
        
        
# class ArticleListCreateView(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticated]
    
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return Article.objects.filter(author=self.request.user)

class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    required_role = 'hod'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    required_role = 'hod'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)
    
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh")
#             if not refresh_token:
#                 return Response({"error": "Refresh token is required."}, status=400)

#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Mark the token as blacklisted

#             return Response({"message": "Logged out successfully."}, status=200)
#         except Exception as e:
#             return Response({"error": "Invalid token or something went wrong."}, status=400)    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist all tokens for the authenticated user
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
                
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)