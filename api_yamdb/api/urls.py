from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    user_signup, CommentViewSet,
    CategoryViewSet, DetailView,
    GenreViewSet, ReviewViewSet,
    TitleViewSet, TokenViewGet,
    UserViewSet)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('users/me/', DetailView.as_view()),
    path('', include(router.urls)),
    path('auth/signup/', user_signup),
    path('auth/token/', TokenViewGet.as_view()),
]
