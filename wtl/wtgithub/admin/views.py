from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST
from wtl.streaming_log_response.response import StreamingLogHttpResponse

from wtl.wtgithub.worker import GithubBulkWorker


@permission_required('wtl.wtgithub_crawl')
@require_POST
def crawl(request):
    crawler = GithubBulkWorker()
    return StreamingLogHttpResponse(crawler.analyze_repos,
                                    logs={'wtl': 'INFO'},
                                    args=[request.REQUEST.get('language')])
