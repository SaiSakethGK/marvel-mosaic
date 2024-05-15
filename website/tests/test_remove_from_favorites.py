from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import FavoriteCharacter

class RemoveFromFavoritesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.character_id = 123

    def test_remove_from_favorites(self):
        response = self.client.post(reverse('remove_from_favorites', args=[self.character_id]))
        self.assertRedirects(response, reverse('view_favorites'))
