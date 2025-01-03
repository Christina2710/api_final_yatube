from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

# Создаём маршрутизатор для автоматической генерации URL-адресов
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'follow', FollowViewSet)
# Позволяет работать с комментариями к конкретному посту
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet
)

urlpatterns = [
    # Подключаем все маршруты, сгенерированные DefaultRouter
    path('v1/', include(router.urls)),
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('v1/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('v1/', include('djoser.urls.jwt'))
]
