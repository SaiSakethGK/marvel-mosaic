from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from website.models import FavoriteCharacter

class AddToFavoritesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_add_to_favorites(self):
        # Ensure character is not initially in favorites
        character_id = 123  # Replace with the character ID you want to test
        self.assertFalse(FavoriteCharacter.objects.filter(user=self.user, character_id=character_id).exists())

        # Make request to add character to favorites
        response = self.client.post(reverse('add_to_favorites', args=[character_id]))

        # Check if character is added to favorites
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(FavoriteCharacter.objects.filter(user=self.user, character_id=character_id).exists())
