from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)


class PostNumberPagination(PageNumberPagination):
    page_size = 3
