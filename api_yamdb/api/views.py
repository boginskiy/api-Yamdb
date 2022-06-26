from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Review
from titles.models import Category, Genre, Title
from .permissions import (
    OnlyReadOrСhangeAuthorAdminModerator,
    AdminOrReadOnly)
from .pagination import CustomPageNumberPagination
from .serializers import (
    CategorySerializer, GenreSerializer,
    ReadTitleSerializer, WriteTitleSerializer,
    ReviewSerializer, CommentSerializer)


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
