import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class PostTagTest(APITestCase):
    fixtures = ['users', 'rareusers', 'categories', 'post_tags', 'tags', 'posts', 'tokens']

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

        # self.assertEqual(json_response[0]["id"], "1")
        self.assertEqual(json_response[0]["post"], 1)
        self.assertEqual(json_response[0]["tag"], 2)
        # self.assertEqual(json_response[1]["id"], "2")
        self.assertEqual(json_response[1]["post"], 2)
        self.assertEqual(json_response[1]["tag"], 4)

    def test_create_post_tag(self):
        url = "/post_tags"
        data = {
            "post": 3,
            "tag": 5
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["post"], 3)
        self.assertEqual(json_response["tag"], 5)
