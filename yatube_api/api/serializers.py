from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        # Эти поля нельзя изменять через API
        read_only_fields = ('author', 'post')


# Сериализатор для работы с группами
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


# Сериализатор для работы с данными пользователя
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        # Доступные значения берутся из модели User
        queryset=User.objects.all(),
        slug_field='username'
    )

    def validate(self, data):
        # Получаем текущего пользователя из контекста запроса
        user = self.context['request'].user
        # Получаем пользователя, на которого создаётся подписка
        following = data['following']

        # Проверяем, что пользователь не подписывается на себя
        if user == following:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя!'
            )

        # Проверяем, что подписка уже существует
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        # Если все проверки прошли успешно, возвращаем данные
        return data

    class Meta:
        fields = '__all__'
        model = Follow
