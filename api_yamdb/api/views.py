from requests import Response
from rest_framework.viewsets import ModelViewSet
from reviews.models import Review, Comment
from django.shortcuts import get_object_or_404
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import OnlyReadOrСhangeAuthorAdminModerator
from .pagination import CustomPageNumberPagination
from rest_framework.views import APIView
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          ReadTitleSerializer, WriteTitleSerializer
                          )
from titles.models import Category, Genre, Title


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
# ------------------------------ Мария


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
        new_queryset = get_object_or_404(Review, id=reviews_id, title_id=titles_id)
        return new_queryset.comments.all()

    def perform_create(self, serializer):
        titles_id = self.kwargs.get('titles_id')
        reviews_id = self.kwargs.get('reviews_id')
        instance = get_object_or_404(Review, id=reviews_id, title_id=titles_id)
        serializer.save(author=self.request.user, review=instance)
# ---------------------------------------

