from rest_framework.pagination import PageNumberPagination
import os


class DefaultPagination(PageNumberPagination):
    page_size = int(os.getenv("API_PAGE_SIZE", "20"))
    page_size_query_param = "page_size"
    max_page_size = 200
