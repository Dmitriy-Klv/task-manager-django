from rest_framework.pagination import CursorPagination


class StandardCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-id'
