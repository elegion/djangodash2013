from django.contrib.auth.decorators import permission_required
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_POST
from wtl.streaming_log_response.middleware import StreamingLogResponseGenerator

from wtl.wtgithub.worker import GithubBulkWorker


@permission_required('wtl.wtgithub_crawl')
@require_POST
def crawl(request):
    crawler = GithubBulkWorker()
    streaming_content = StreamingLogResponseGenerator(crawler.analyze_repos,
                                                      logs={'wtl': 'DEBUG'},
                                                      args=[request.REQUEST.get('language')])
    return StreamingHttpResponse(streaming_content)
