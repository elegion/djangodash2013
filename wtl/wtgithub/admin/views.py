from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from wtl.wtgithub.worker import GithubBulkWorker


@permission_required('wtl.wtgithub_crawl')
@require_POST
def crawl(request):
    crawler = GithubBulkWorker()
    crawler.analyze_repos(request.REQUEST.get('language'))
    return HttpResponse('Ok!')
