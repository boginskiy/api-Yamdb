from rest_framework import serializers
from reviews.models import Review, Comment
from rest_framework.validators import UniqueTogetherValidator


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs.get('titles_id')

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        )
    title = serializers.HiddenField(default=CurrentTitleDefault(),)

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
        UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('author', 'title'),
            message = 'Не более одного комментария для произведения'
        )
    ]

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Поставьте оценку от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',)

    class Meta:
        exclude = ('review',)
        model = Comment
#----------------------------------------------
