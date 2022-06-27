from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.service import send_code_to_email, get_tokens_for_user
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
        model = User


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'email']
        model = User

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            confirmation_code=self.context["code"]
        )
        user.save()
        send_code_to_email(self.context["code"], validated_data['email'])
        return user

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Имя 'me' нельзя использовать")
        return data


class TokenSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        try:
            if user.confirmation_code == int(confirmation_code):
                token = get_tokens_for_user(user)
            else:
                raise serializers.ValidationError(
                    {"o-ops": "Неправильный проверочный код"}
                )
        except:
            raise serializers.ValidationError(
                {"o-ops": "Забыли указать проверочный код"}
            )

        return {
            'token_refresh': token['refresh'],
            'token_access': token['access']
        }

    def to_representation(self, instance):
        return {
            'refresh': instance['token_refresh'],
            'access': instance['token_access']
        }
