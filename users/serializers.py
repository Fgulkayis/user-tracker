

from rest_framework import serializers
from .models import User, Post, Comment, Album, Photo, Todo

class UserSerializer(serializers.ModelSerializer):
    # Kullanıcının ilişkili olduğu verileri de göstermek için iç içe serileştiriciler
    # read_only=True: Bu alanların sadece okunabilir olmasını sağlar, doğrudan oluşturulamaz/güncellenemez
    # many=True: Birden fazla ilişki (bir kullanıcı birden fazla gönderi, albüm, görev vb. sahip olabilir)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    albums = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    todos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'website', 'phone', 'posts', 'albums', 'todos']
        # 'fields' yerine '__all__' de kullanabilirdik, ancak belirli alanları belirtmek daha kontrollüdür.

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' # Tüm alanları dahil et
        # 'user' alanı burada otomatik olarak id olarak gelecektir.
        # Eğer kullanıcı detaylarını da görmek istersek, UserSerializer'ı iç içe kullanabiliriz.
        # user = UserSerializer(read_only=True) şeklinde bir ekleme yapılabilir.

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'