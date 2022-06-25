from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

router.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]