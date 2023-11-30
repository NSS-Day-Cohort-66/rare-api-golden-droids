import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class PostTagTest(APITestCase):
    fixtures = ['tags', 'users', 'posts', 'tokens']

    def setUp(self):