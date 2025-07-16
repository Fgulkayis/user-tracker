

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache # Önbellek modülünü import ediyoruz

from .models import User, Post, Comment, Album, Photo, Todo
from .serializers import (
    UserSerializer, PostSerializer, CommentSerializer,
    AlbumSerializer, PhotoSerializer, TodoSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Bir kullanıcının tüm paylaşımlarını getiren özel aksiyon
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        # Önbellek anahtarı oluştur
        cache_key = f'user_{user.id}_posts'
        # Önbellekten veriyi çekmeye çalış
        posts_data = cache.get(cache_key)

        if posts_data is None:
            # Veri önbellekte yoksa, veritabanından çek ve önbelleğe kaydet
            posts = user.posts.all()
            serializer = PostSerializer(posts, many=True)
            posts_data = serializer.data
            # 60 saniye (veya istediğiniz süre) önbellekte tut
            cache.set(cache_key, posts_data, timeout=60)
            print(f"Veri veritabanından çekildi ve önbelleğe kaydedildi: {cache_key}")
        else:
            print(f"Veri önbellekten çekildi: {cache_key}")

        return Response(posts_data)

    # Benzer şekilde diğer action metodlarını da aynı mantıkla güncelleyin:
    # albums, todos, comments, photos

    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        user = self.get_object()
        cache_key = f'user_{user.id}_albums'
        albums_data = cache.get(cache_key)
        if albums_data is None:
            albums = user.albums.all()
            serializer = AlbumSerializer(albums, many=True)
            albums_data = serializer.data
            cache.set(cache_key, albums_data, timeout=60)
            print(f"Veri veritabanından çekildi ve önbelleğe kaydedildi: {cache_key}")
        else:
            print(f"Veri önbellekten çekildi: {cache_key}")
        return Response(albums_data)

    @action(detail=True, methods=['get'])
    def todos(self, request, pk=None):
        user = self.get_object()
        cache_key = f'user_{user.id}_todos'
        todos_data = cache.get(cache_key)
        if todos_data is None:
            todos = user.todos.all()
            serializer = TodoSerializer(todos, many=True)
            todos_data = serializer.data
            cache.set(cache_key, todos_data, timeout=60)
            print(f"Veri veritabanından çekildi ve önbelleğe kaydedildi: {cache_key}")
        else:
            print(f"Veri önbellekten çekildi: {cache_key}")
        return Response(todos_data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        user = self.get_object()
        cache_key = f'user_{user.id}_comments'
        comments_data = cache.get(cache_key)
        if comments_data is None:
            user_posts = user.posts.all()
            all_comments = Comment.objects.filter(post__in=user_posts)
            serializer = CommentSerializer(all_comments, many=True)
            comments_data = serializer.data
            cache.set(cache_key, comments_data, timeout=60)
            print(f"Veri veritabanından çekildi ve önbelleğe kaydedildi: {cache_key}")
        else:
            print(f"Veri önbellekten çekildi: {cache_key}")
        return Response(comments_data)

    @action(detail=True, methods=['get'])
    def photos(self, request, pk=None):
        user = self.get_object()
        cache_key = f'user_{user.id}_photos'
        photos_data = cache.get(cache_key)
        if photos_data is None:
            user_albums = user.albums.all()
            all_photos = Photo.objects.filter(album__in=user_albums)
            serializer = PhotoSerializer(all_photos, many=True)
            photos_data = serializer.data
            cache.set(cache_key, photos_data, timeout=60)
            print(f"Veri veritabanından çekildi ve önbelleğe kaydedildi: {cache_key}")
        else:
            print(f"Veri önbellekten çekildi: {cache_key}")
        return Response(photos_data)


class PostViewSet(viewsets.ModelViewSet):
    # ... (bu kısım değişmedi) ...
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    # ... (bu kısım değişmedi) ...
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    # ... (bu kısım değişmedi) ...
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class PhotoViewSet(viewsets.ModelViewSet):
    # ... (bu kısım değişmedi) ...
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    # ... (bu kısım değişmedi) ...
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer