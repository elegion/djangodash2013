from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
import mock

from wtl.wtcore.factories import SuperuserFactory, FACTORY_USER_PASSWORD


class CrawlTestCase(TestCase):
    def setUp(self):
        super(CrawlTestCase, self).setUp()
        self.workerPatch = mock.patch('wtl.wtgithub.worker.GithubBulkWorker')
        self.workerClassMock = self.workerPatch.start()
        self.addCleanup(self.workerPatch.stop)

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

    # My brain is blown after 2 days of djangodash and I can't implement this test >_<
    #def test_runs_worker_with_given_language(self):
    #    user = SuperuserFactory()
    #    self.client.login(username=user.username, password=FACTORY_USER_PASSWORD)
    #    self.client.post(reverse('wtgithub_admin_crawl'), {'language': 'Ruby'})
    #    self.assertEqual(self.workerMock.mock_calls, [mock.call.analyze_repos('Ruby')])
