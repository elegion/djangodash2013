from wtl.wtlib.models import Language


def languages(request):
    return {'languages': Language.objects.all()}
