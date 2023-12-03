from rest_framework import pagination
from rest_framework.response import Response


class BasePagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        self.respose_items = {}
        self.respose_items["count_all"] = queryset.count()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response = {
            "total": self.page.paginator.num_pages,
            "results": data,
        }
        response.update(self.respose_items)
        return Response(response)
