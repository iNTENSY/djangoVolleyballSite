from django.test import TestCase
from django.urls import reverse

from .models import Teams

class TeamsListTestCase(TestCase):
    def test_view(self):
        path = reverse('rating:teamlist')
        response = self.client.get(path)

        print(response)
