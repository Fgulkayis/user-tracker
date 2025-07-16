from django.db import models

# Create your models here.
class User(models.Model):
    name =models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
   
    def __str__(self):
        return self.username

class Post(models.Model):
    """
    Kullanıcı paylaşımlarını (gönderilerini) tutan model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title[:30]}...'

class Comment(models.Model):
    """
    Paylaşımlara yapılan yorumları tutan model.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100) # Yorum yapanın adı (eğer user modeli ile ilişkili değilse)
    email = models.EmailField() # Yorum yapanın e-postası
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title[:20]}...'

class Album(models.Model):
    """
    Kullanıcılara ait albümleri tutan model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    """
    Albümlerin içerisindeki fotoğrafları tutan model.
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=200)
    url = models.URLField() # Fotoğrafın URL'si
    thumbnail_url = models.URLField(blank=True, null=True) # Küçük resim URL'si
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Todo(models.Model):
    """
    Kullanıcılara ait görev listesini (yapılacaklar listesi) tutan model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False) # Görevin tamamlanıp tamamlanmadığı
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True) # Görev bitiş tarihi

    def __str__(self):
        return f'{self.title} - {"Completed" if self.completed else "Pending"}'