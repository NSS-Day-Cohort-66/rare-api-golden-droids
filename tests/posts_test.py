import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import datetime


class PostTest(APITestCase):
    # Add any fixtures you want to run to build the test database
    fixtures = ['posts', 'users', 'tokens', 'rareusers', 'reactions', 'post_reactions', 'categories']

    def setUp(self):
        self.user = User.objects.first()
        self.user.is_staff = True
        self.user.save()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_single_post(self):
        """Ensure we can retrieve an existing post
        """
        # Initiate request and store response
        response = self.client.get(f"/posts/1")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the post was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        keys = {'id', 'title', 'rare_user', 'category', 'publication_date', 'content', 'post_reactions', 'approved'}
        self.assertEqual(json_response.keys(), keys)

    def test_get_all_posts(self):
        """Ensure we can list existing posts
        """
        # Initiate request and store response
        response = self.client.get(f"/posts")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the post was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        date = json_response[0]["publication_date"]
        now = datetime.date.today()
        current_date = now.strftime("%m-%d-%Y")
        self.assertFalse(date == current_date)

    def test_delete_single_post(self):
        """
        Ensure we can delete an existing post.
        """
        # DELETE the post you just created
        response = self.client.delete(f"/posts/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the post again to verify you get a 404 response
        response = self.client.get(f"/posts/1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
