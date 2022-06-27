from rest_framework import (viewsets, filters, generics, status,
                            serializers)
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.service import get_random_number
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Review
from user.models import User
from titles.models import Category, Genre, Title
from .permissions import (
    OnlyReadOrСhangeAuthorAdminModerator,
    AdminOrReadOnly)
from .pagination import CustomPageNumberPagination, CustomPagination
from .serializers import (
    CategorySerializer, GenreSerializer,
    ReadTitleSerializer, WriteTitleSerializer,
    ReviewSerializer, CommentSerializer,
    UserSerializer, AuthSerializer,
    TokenSerializer)


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = WriteTitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WriteTitleSerializer
        return ReadTitleSerializer

    def get_queryset(self):
        new_queryset = Title.objects.annotate(
            rating=models.Sum(models.F('reviews__score'))
            / models.Count(models.F('reviews'))
        )
        return new_queryset


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OnlyReadOrСhangeAuthorAdminModerator,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        titles_id = self.kwargs.get('titles_id')
        new_queryset = get_object_or_404(Title, id=titles_id)
        return new_queryset.reviews.all()

    def perform_create(self, serializer):
        titles_id = self.kwargs.get('titles_id')
        instance = get_object_or_404(Title, id=titles_id)
        serializer.save(author=self.request.user, title=instance)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OnlyReadOrСhangeAuthorAdminModerator,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        titles_id = self.kwargs.get('titles_id')
        reviews_id = self.kwargs.get('reviews_id')
        new_queryset = get_object_or_404(
            Review,
            id=reviews_id,
            title_id=titles_id)
        return new_queryset.comments.all()

    def perform_create(self, serializer):
        titles_id = self.kwargs.get('titles_id')
        reviews_id = self.kwargs.get('reviews_id')
        instance = get_object_or_404(Review, id=reviews_id, title_id=titles_id)
        serializer.save(author=self.request.user, review=instance)
  