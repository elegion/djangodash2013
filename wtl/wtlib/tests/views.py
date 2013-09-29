from __future__ import unicode_literals

from django.test import TestCase


class HomeTestCase(TestCase):
    def test_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('wtlib/home.html')
        self.assertTemplateUsed('wtlib/_repo_form.html')
