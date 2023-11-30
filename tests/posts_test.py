import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rareapi.models import Post, RareUser, Category



class PostTest(APITestCase):
    # Add any fixtures you want to run to build the test database
    fixtures = ['posts', 'users', 'tokens', 'rareusers', 'categories']

    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = RareUser.objects.get(user=self.user)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_delete_post(self):
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
        post.image_url = "https://example.com/image6.jpg"
        post.content = "This is a test"
        post.approved = True

        data = {
            "categoryId": 3,
            "title": "Test Post",
            "image_url": "https://example.com/image1.jpg",
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
        self.assertEqual(json_response["image_url"], "https://example.com/image1.jpg")
        self.assertEqual(json_response["content"], "This is a test.")
        self.assertTrue(json_response["approved"])

    def test_get_filtered_posts(self):
        """Ensure we can get a list of of current user's posts
        """

        response = self.client.get(f"/posts?rare_user=current")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for post in json_response:
            print(post["rare_user"]["id"])
            if post["rare_user"]["id"] != self.rare_user.id:
                self.fail("Unexpected post for another user found in the response.")