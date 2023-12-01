import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rareapi.models import Post, RareUser, Category
import datetime


class PostTest(APITestCase):
    # Add any fixtures you want to run to build the test database
    fixtures = ['posts', 'users', 'tokens', 'rareusers', 'reactions', 'post_reactions', 'categories']

    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = RareUser.objects.get(user=self.user)
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
        keys = {'id', 'title', 'rare_user', 'category', 'publication_date','image_url', 'content', 'post_reactions', 'approved', 'post_tags'}
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

    def test_change_post(self):
        """
        Ensure we can change an existing post.
        """
        post = Post()
        post.rare_user = RareUser.objects.get(user_id=self.user.id)
        post.category = Category.objects.get(pk=2)
        post.title = "Test"
        post.image_url = None
        post.content = "This is a test"
        post.approved = True

        data = {
            "categoryId": 3,
            "title": "Test Post",
            "image_url": None,
            "content": "This is a test."
        }

        response = self.client.put(f"/posts/1", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/posts/1")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["rare_user"]["id"], self.rare_user.id)
        self.assertEqual(json_response["title"], "Test Post")
        self.assertEqual(json_response["category"]["label"], "Traveling")
        self.assertEqual(json_response["image_url"], None)
        self.assertEqual(json_response["content"], "This is a test.")
        self.assertTrue(json_response["approved"])

    def test_get_filtered_posts(self):
        """Ensure we can get a list of of current user's posts
        """

        response = self.client.get(f"/posts?rare_user=current")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for post in json_response:
            if post["rare_user"]["id"] != self.rare_user.id:
                self.fail("Unexpected post for another user found in the response.")