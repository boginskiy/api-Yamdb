from rest_framework import (viewsets, filters, generics, status,
                            serializers)
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.paginations import CustomPagination
from api.serializer import UserSerializer, AuthSerializer, TokenSerializer
from api.service import get_random_number
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Viewsets для всех пользователей."""
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ['username']
    pagination_class = CustomPagination


class DetailView(APIView):
    """Получение и изменение данных своей учетной записи"""
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthViewRegister(generics.CreateAPIView):
    """Регистрация пользователя."""
    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super(AuthViewRegister, self).get_serializer_context()
        code = get_random_number()
        context.update({"code": code})
        return context


class TokenViewGet(APIView):
    """Получаем токен."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
