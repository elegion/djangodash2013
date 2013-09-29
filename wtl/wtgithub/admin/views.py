from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@permission_required('wtl.wtgithub_crawl')
@require_POST
def crawl(request):
    return HttpResponse('Ok!')
