from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1 
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        page_count = self.page.paginator.num_pages
        return Response({
            'page_count': page_count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })