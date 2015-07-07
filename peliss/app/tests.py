"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase
from django.test import Client

from datetime import datetime, timedelta, date
from app.models import User, Film, SeenFilm, News, WantedFilm



# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            django.setup()

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 1, 200)

    def test_logging(self):
        c = Client()
        response = c.post('/login/', {'username': 'andres', 'password': 'django'})
        self.assertEqual(response.status_code, 302)
        
    def test_mispeliss(self):
        c = Client()
        seen = SeenFilm.objects.get(user=1)
        visto = seen.films.all()
        response = c.post('/misPelis/')
        self.assertEqual(response.status_code, 200)

    def test_film(self):
        c = Client()
        response = c.post('/film/Gladiator')
        self.assertEqual(response.status_code, 200)