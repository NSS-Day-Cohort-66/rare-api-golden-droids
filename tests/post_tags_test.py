import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class PostTagTest(APITestCase):
    fixtures = ['tags', 'users', 'posts', 'tokens']

    def setUp(self):
        self.user = User.objects.first()
        self.user.is_staff = True
        self.user.save()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_tags(self):
        response = self.client.get(f"/post_tags")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response[0]["id"], "1")
        self.assertEqual(json_response[0]["post_id"], "1")
        self.assertEqual(json_response[0]["tag_id"], "2")
        self.assertEqual(json_response[1]["id"], "2")
        self.assertEqual(json_response[1]["post_id"], "2")
        self.assertEqual(json_response[1]["tag_id"], "4")