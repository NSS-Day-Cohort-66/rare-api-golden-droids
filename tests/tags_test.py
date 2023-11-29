import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class TagTest(APITestCase):
    fixtures = ['tags', 'users', 'tokens']

    def setUp(self):
        self.user = User.objects.first()
        self.user.is_staff = True
        self.user.save()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_tag(self):
        url = "/tags"

        data = {
            "label": "Test Tag"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["label"], "Test Tag")