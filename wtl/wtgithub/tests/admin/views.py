from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from wtl.wtcore.factories import SuperuserFactory, FACTORY_USER_PASSWORD


class CrawlTestCase(TestCase):
    def test_anonymous(self):
        url = reverse('wtgithub_admin_crawl')
        response = self.client.get(url)
        self.assertRedirects(response, settings.LOGIN_URL + '?next=%s' % url)

    def test_post_required(self):
        user = SuperuserFactory()
        self.client.login(username=user.username, password=FACTORY_USER_PASSWORD)
        response = self.client.get(reverse('wtgithub_admin_crawl'))
        self.assertEqual(405, response.status_code)

    def test_responds_ok(self):
        user = SuperuserFactory()
        self.client.login(username=user.username, password=FACTORY_USER_PASSWORD)
        response = self.client.post(reverse('wtgithub_admin_crawl'))
        self.assertContains(response, 'Ok!')
