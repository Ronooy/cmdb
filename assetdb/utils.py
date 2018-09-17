#!/usr/bin/env python
from django.core.paginator import Paginator


def paginated(query_set, page=None, limit=None):

    try:
        paginator = Paginator(query_set, int(limit))
    except Exception:
        paginator = Paginator(query_set, 10)
    try:
        pageObj = paginator.page(int(page))
    except:
        pageObj = paginator.page(1)
    return paginator, pageObj