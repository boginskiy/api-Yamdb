from django.urls import path, include
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/me/', DetailView.as_view()),
    path('', include(router.urls)),
    path('auth/signup/', AuthViewRegister.as_view()),
    path('auth/token/', TokenViewGet.as_view(), name='TokenViewGet'),
]
