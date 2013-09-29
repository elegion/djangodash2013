from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(items, per, page):
    paginator = Paginator(items, per)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
