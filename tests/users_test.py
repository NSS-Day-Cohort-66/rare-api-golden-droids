import json
from rest_framework import status
from rest_framework.test import APITestCase
from rareapi.models import RareUser
from django.contrib.auth.models import User

class UserTest(APITestCase):
    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'rareusers']

    def test_create_registration(self):
        """
        Ensure we can register a user
        """

        # Define the endpoint in the API to which
        # the request will be sent
        url = "/register"

        # Define the request body
        data = {
            "first_name": "Tricia",
            "last_name": "Swift",
            "username": "triciaswift",
            "email": "tricia@swift.com",
            "password": "swift",
            "bio": "I like dogs"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response body contains the expected keys
        expected_keys = {'valid', 'token', 'staff'}
        self.assertEqual(set(response.data.keys()), expected_keys)

        # Check the user properties in database
        user = User.objects.get(username='triciaswift')
        self.assertEqual(user.first_name, "Tricia")
        self.assertEqual(user.last_name, "Swift")
        self.assertEqual(user.email, "tricia@swift.com")
        self.assertFalse(user.is_staff)

        # Check the rare_user properties in database
        rare_user = RareUser.objects.get(bio='I like dogs')
        self.assertEqual(rare_user.user_id, user.id)
        
    def test_create_login(self):
        """
        Ensure we can login a user
        """

        # Define the endpoint in the API to which
        # the request will be sent
        url = "/login"

        # Define the request body
        data = {
            "username": "phifertristan",
            "password": "phifer"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response body contains the expected keys
        # Assert that the properties on the created resource are correct
        self.assertTrue(json_response['valid'])
        self.assertEqual(json_response['token'], "978afa7b76527cc21d76d7b5430ab77f73aa3bff")
        self.assertTrue(json_response['staff'])
