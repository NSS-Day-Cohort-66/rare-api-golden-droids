import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class CategoryTest(APITestCase):
    # Add any fixtures you want to run to build the test database
    fixtures = ['categories', 'users', 'tokens']

    def setUp(self):
        self.user = User.objects.first()
        self.user.is_staff = True
        self.user.save()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_category(self):
        """
        Ensure we can create a new category
        """

        # Define the endpoint in the API to which
        # the request will be sent
        url = "/categories"

        # Define the request body
        data = {
            "label": "Test Category"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["label"], "Test Category")

    def test_get_a_single_category(self):
        """Ensure we can get an existing category
        """

        # Initiate request and store response
        response = self.client.get(f"/categories/1")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Lifestyle")

    def test_get_all_categories(self):
        """Ensure we can get a list of existing categories
        """

        # Initiate request and store response
        response = self.client.get(f"/categories")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response[0]["label"], "Cooking")
        self.assertEqual(json_response[2]["label"], "Traveling")

    def test_change_category(self):
        """
        Ensure we can change an existing category.
        """

        # DEFINE NEW PROPERTIES FOR CATEGORY
        data = {
            "label": "Dogs"
        }

        response = self.client.put(f"/categories/1", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET category again to verify changes were made
        response = self.client.get(f"/categories/1")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Dogs")

    def test_delete_category(self):
        """
        Ensure we can delete an existing category.
        """

        # DELETE the category you just created
        response = self.client.delete(f"/categories/1")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the category again to verify you get a 404 response
        response = self.client.get(f"/categories/1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)