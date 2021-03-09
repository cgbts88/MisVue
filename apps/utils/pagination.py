from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from math import ceil


class CommonPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        filters = "&".join([item[0] + '=' + item[1] for item in self.request.GET.items() if item[0] != 'page'])

        around_count = 1
        total_page = ceil(self.page.paginator.count/self.page_size)
        cur_page = self.page.number
        pages_num = []

        if cur_page <= around_count + 2:
            left_page = range(1, cur_page)
        else:
            left_page = (1, '...', cur_page-1)
        for page in left_page:
            pages_num.append(page)

        pages_num.append(str(cur_page))

        if total_page <= cur_page + 2:
            right_page = range(cur_page + 1, total_page + 1)
        else:
            right_page = (cur_page + 1, '...', total_page)
        for page in right_page:
            pages_num.append(page)

        pages = []
        for page in pages_num:
            if not isinstance(page, int) or page == cur_page:
                pages.append({'num': page, 'link': None})
            elif len(filters):
                pages.append({'num': page, 'link': '?page={}&{}'.format(page, filters)})
            else:
                pages.append({'num': page, 'link': '?page={}'.format(page)})

        return Response(OrderedDict([
            ('results', data),
            ('pages', pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
        ]))
