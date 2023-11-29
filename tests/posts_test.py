import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class PostTest(APITestCase):
    # Add any fixtures you want to run to build the test database
    fixtures = ['posts', 'users', 'tokens']

    def setUp(self):
        self.user = User.objects.first()
        self.user.is_staff = True
        self.user.save()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_post(self):
        """
        Ensure we can create a new post
        """

        # Define the endpoint in the API to which
        # the request will be sent
        url = "/posts"

        # Define the request body
        data = {
            "label": "Test Post"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["label"], "Test Post")

    def test_get_post(self):
        """Ensure we can get an existing post
        """

        # Initiate request and store response
        response = self.client.get(f"/posts/1")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Lifestyle")

    def test_get_posts(self):
        """Ensure we can get a list of existing posts
        """

        # Initiate request and store response
        response = self.client.get(f"/posts")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response[0]["label"], "Cooking")
        self.assertEqual(json_response[1]["label"], "Lifestyle")

    def test_change_post(self):
        """
        Ensure we can change an existing post.
        """

        # DEFINE NEW PROPERTIES FOR CATEGORY
        data = {
            "label": "Dogs"
        }

        response = self.client.put(f"/posts/1", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET post again to verify changes were made
        response = self.client.get(f"/posts/1")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Dogs")

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