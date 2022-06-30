import random
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from api_yamdb import settings


def get_random_number() -> str:
    """Возвращает случайное число в виде строки."""
    num = random.randint(100000, 999999)
    return str(num)


def send_code_to_email(code: str, email: str) -> None:
    """Отправлем код с подтверждением на почту"""
    send_mail('Код подтверждения', code,
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)
    return None


def get_tokens_for_user(user: object) -> dict:
    """Возвращаем токен"""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
