from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """
    customize view pagination
    page_size to zero if you want the minimum size (10)
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000
