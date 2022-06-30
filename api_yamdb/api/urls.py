from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TitleViewSet, CategoryViewSet,
    GenreViewSet, ReviewViewSet,
    CommentViewSet, DetailView,
    AuthViewRegister, TokenViewGet,
    UserViewSet)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [

    path('users/me/', DetailView.as_view()),
    path('', include(router.urls)),
    path('auth/signup/', AuthViewRegister.as_view()),
    path('auth/token/', TokenViewGet.as_view()),
]
