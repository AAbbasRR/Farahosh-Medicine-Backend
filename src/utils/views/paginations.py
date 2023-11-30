from rest_framework import pagination
from rest_framework.response import Response

from app_notification.models import ResellerNotificationModel


class BasePagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        self.respose_items = {}
        self.respose_items["count_all"] = queryset.count()
        if queryset.model == ResellerNotificationModel:
            self.respose_items["unread_count"] = queryset.filter(is_read=False).count()

        # try:
        #    self.available_products_count = queryset.filter(
        #        warehouse_status="avl"
        #    ).count()
        # except:
        #    self.available_products_count = None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response = {
            "total": self.page.paginator.num_pages,
            "results": data,
        }
        response.update(self.respose_items)
        return Response(response)
