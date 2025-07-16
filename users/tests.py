

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Post, Comment, Album, Photo, Todo

class UserAPITests(APITestCase):
    def setUp(self):
        # Her test çalıştırılmadan önce çağrılır.
        # Test için gerekli örnek verileri burada oluşturuyoruz.
        self.user1 = User.objects.create(
            name='Alice', username='alice', email='alice@example.com'
        )
        self.user2 = User.objects.create(
            name='Bob', username='bob', email='bob@example.com'
        )
        self.post1 = Post.objects.create(
            user=self.user1, title='Alice\'s First Post', body='Content of Alice\'s first post.'
        )
        self.post2 = Post.objects.create(
            user=self.user1, title='Alice\'s Second Post', body='Content of Alice\'s second post.'
        )
        self.post3 = Post.objects.create(
            user=self.user2, title='Bob\'s Post', body='Content of Bob\'s post.'
        )
        self.comment1 = Comment.objects.create(
            post=self.post1, name='Commenter1', email='c1@example.com', body='Great post!'
        )
        self.comment2 = Comment.objects.create(
            post=self.post2, name='Commenter2', email='c2@example.com', body='Nice one!'
        )
        self.album1 = Album.objects.create(
            user=self.user1, title='Alice\'s Holiday Album'
        )
        self.album2 = Album.objects.create(
            user=self.user2, title='Bob\'s Photos'
        )
        self.photo1 = Photo.objects.create(
            album=self.album1, title='Sunset', url='http://example.com/sunset.jpg'
        )
        self.photo2 = Photo.objects.create(
            album=self.album1, title='Beach', url='http://example.com/beach.jpg'
        )
        self.todo1 = Todo.objects.create(
            user=self.user1, title='Buy groceries', completed=False
        )
        self.todo2 = Todo.objects.create(
            user=self.user1, title='Walk the dog', completed=True
        )
        self.todo3 = Todo.objects.create(
            user=self.user2, title='Pay bills', completed=False
        )

    def test_list_users(self):
        """
        Tüm kullanıcıları listeleme endpoint'ini test eder.
        """
        response = self.client.get(reverse('user-list')) # user-list, router tarafından otomatik oluşturulan isimdir.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # İki kullanıcı oluşturmuştuk

    def test_retrieve_user(self):
        """
        Belirli bir kullanıcıyı getirme endpoint'ini test eder.
        """
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'alice')

    def test_create_user(self):
        """
        Yeni bir kullanıcı oluşturma endpoint'ini test eder.
        """
        data = {'name': 'Charlie', 'username': 'charlie', 'email': 'charlie@example.com'}
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.data['username'], 'charlie')

    def test_update_user(self):
        """
        Kullanıcı bilgilerini güncelleme endpoint'ini test eder.
        """
        data = {'name': 'Alicia', 'username': 'alice_updated', 'email': 'alice_updated@example.com'}
        response = self.client.put(reverse('user-detail', kwargs={'pk': self.user1.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db() # Veritabanındaki değişikliği al
        self.assertEqual(self.user1.username, 'alice_updated')

    def test_delete_user(self):
        """
        Kullanıcı silme endpoint'ini test eder.
        """
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1) # user1 silindiği için 1 kullanıcı kaldı (user2)

    # --- Özel Aksiyon Testleri ---

    def test_user_posts_action(self):
        """
        Bir kullanıcının paylaşımlarını getiren özel aksiyonu test eder.
        """
        response = self.client.get(reverse('user-posts', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Alice'in 2 postu vardı
        self.assertEqual(response.data[0]['title'], 'Alice\'s First Post')

    def test_user_albums_action(self):
        """
        Bir kullanıcının albümlerini getiren özel aksiyonu test eder.
        """
        response = self.client.get(reverse('user-albums', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Alice'in 1 albümü vardı
        self.assertEqual(response.data[0]['title'], 'Alice\'s Holiday Album')

    def test_user_todos_action(self):
        """
        Bir kullanıcının görevlerini getiren özel aksiyonu test eder.
        """
        response = self.client.get(reverse('user-todos', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Alice'in 2 görevi vardı
        self.assertEqual(response.data[0]['title'], 'Buy groceries')

    def test_user_comments_action(self):
        """
        Bir kullanıcının yorumlarını getiren özel aksiyonu test eder.
        """
        response = self.client.get(reverse('user-comments', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Alice'in postlarına 2 yorum vardı
        self.assertEqual(response.data[0]['body'], 'Great post!')

    def test_user_photos_action(self):
        """
        Bir kullanıcının fotoğraflarını getiren özel aksiyonu test eder.
        """
        response = self.client.get(reverse('user-photos', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Alice'in albümünde 2 fotoğraf vardı
        self.assertEqual(response.data[0]['title'], 'Sunset')