from rest_framework import viewsets, permissions
# from rest_framework import filters
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow, User
from .serializers import (PostSerializer, CommentSerializer,
                          GroupSerializer, UserSerializer, FollowSerializer)


# ViewSet для управления публикациями
class PostViewSet(viewsets.ModelViewSet):
    # Указываем, какие объекты обрабатываются и каким сериализатором
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Переопределяем сохранение объекта
    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как автора поста
        serializer.save(author=self.request.user)

    # Переопределяем обновление объекта
    def perform_update(self, serializer):
        # Проверяем, что пользователь - автор поста
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        # Если авторизация пройдена, вызываем стандартное обновление
        super(PostViewSet, self).perform_update(serializer)

    # Переопределяем удаление объекта
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(instance)


# ViewSet для управления комментариями
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # Получаем пост, к которому относятся комментарии
    def get_post(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return post

    # Получаем только комментарии, относящиеся к конкретному посту
    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(post=post, author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)


# ViewSet для управления группами (только чтение)
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# ViewSet для управления пользователями
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ViewSet для управления подписками
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # Подключаем фильтр для поиска по полям
    # filter_backends = (filters.SearchFilter,)
    # Фильтруем по имени пользователя, на которого подписываются
    # search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        # Возвращаем подписки текущего пользователя
        queryset = user.follower.all()
        # Получаем параметр поиска из GET-запроса
        search_query = self.request.query_params.get('search', None)
        if search_query:
            # Фильтруем по имени пользователя, на которого подписываются
            queryset = queryset.filter(
                following__username__icontains=search_query
            )
        return queryset

    def perform_create(self, serializer):
        # Сохраняем данные, передавая текущего пользователя как автора подписки
        serializer.save(user=self.request.user)
