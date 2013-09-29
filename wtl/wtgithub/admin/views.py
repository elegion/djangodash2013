from django.contrib.auth.decorators import permission_required
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_POST
from wtl.streaming_log_response.generator import StreamingLogResponseGenerator

from wtl.wtgithub.worker import GithubBulkWorker


@permission_required('wtl.wtgithub_crawl')
@require_POST
def crawl(request):
    crawler = GithubBulkWorker()
    def on_success(checked_repos, new_repos, analyzed_repos):
        return '<h2>Finished crawling. %i repositories checked ' \
               '(%i new, %i successfully analysed)</h2>' % (checked_repos, new_repos, analyzed_repos)
    streaming_content = StreamingLogResponseGenerator(crawler.analyze_repos,
                                                      logs={'wtl': 'DEBUG'},
                                                      args=[request.REQUEST.get('language')],
                                                      callback=on_success)
    return StreamingHttpResponse(streaming_content)
