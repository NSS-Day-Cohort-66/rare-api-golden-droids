import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class CommentTest(APITestCase):
    fixtures = ['comments', 'users', 'tokens', 'posts', 'rareusers', 'categories']

    def setUp(self):
        self.user = User.objects.first()
        self.user.is_staff = True
        self.user.save()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_comments(self):
        """Ensure we can get a list of existing categories
        """

        # Initiate request and store response
        response = self.client.get(f"/comments")

            # Parse the JSON in the response body
        json_response = json.loads(response.content)

            # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Assert that the values are correct
        self.assertEqual(json_response[0]["content"], "Are you serious?")
        self.assertEqual(json_response[1]["content"], "Love!")


    def test_create_comment(self):
        """
        Ensure we can create a new comment
        """

        # Define the endpoint in the API to which
        # the request will be sent
        url = "/comments"

        # Define the request body
        data = {
            "postId": 2,
            "author": 1,
            "content": "test comment"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["post"], 2)
        self.assertEqual(json_response["author"]["user"]["full_name"], "Carrie Belk")
        self.assertEqual(json_response["content"], "test comment")
       

    def test_delete_comment(self):
        """
        Ensure we can delete an existing category.
        """

        # DELETE the category you just created
        response = self.client.delete(f"/comments/2")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        
         # Initiate request and store response
        response = self.client.get(f"/comments")

            # Parse the JSON in the response body
        json_response = json.loads(response.content)

            # Assert that the values are correct
            # checking to make sure the get all doesn't include 2 at index 3 because we don't have retrieve method currently
        self.assertIsNot(json_response[3]["id"], 2)
        