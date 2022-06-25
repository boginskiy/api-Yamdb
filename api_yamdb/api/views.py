from requests import Response
from rest_framework.viewsets import ModelViewSet
from reviews.models import Review, Comment
from titles.models import Title
from django.shortcuts import get_object_or_404
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import OnlyReadOrСhangeAuthorAdminModerator
from .pagination import CustomPageNumberPagination
from rest_framework.views import APIView
from django.db import models


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
