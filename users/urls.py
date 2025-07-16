
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PostViewSet, CommentViewSet,
    AlbumViewSet, PhotoViewSet, TodoViewSet
)

# Bir router oluşturuyoruz ve ViewSet'lerimizi bu router'a kaydediyoruz.
# Router, otomatik olarak URL kalıplarını oluşturur (listeleme, detay vb.).
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'todos', TodoViewSet)

urlpatterns = [
    # Router tarafından oluşturulan URL'leri dahil ediyoruz
    path('', include(router.urls)),
]