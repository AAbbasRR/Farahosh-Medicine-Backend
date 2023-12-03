from rest_framework import response

from app_medicine.api.user.serializers.medicine import (
    UserListMedicineSerializer,
    UserDetailMedicineSerializer,
)
from app_medicine.models import MedicineModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.paginations import BasePagination
from utils.views.permissions import IsAuthenticatedPermission
from utils.classes import Redis, RedisKeys


class UserListWithPaginationMedicineAPIVIew(generics.CustomListAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = UserListMedicineSerializer
    search_fields = ["brand_code", "title", "shape", "dose"]
    queryset = MedicineModel.objects.all().order_by("title")


class UserListAllMedicineAPIVIew(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning

    def get(self, *args, **kwargs):
        redis_cache_service = Redis("medicine", RedisKeys.list_all_data)
        if not redis_cache_service.exists():
            all_medicine = MedicineModel.objects.all().order_by("title")
            serializer_medicine_data = UserDetailMedicineSerializer(
                all_medicine, many=True
            ).data
            redis_cache_service.set_json_value(serializer_medicine_data)
        data = redis_cache_service.get_json_value()
        return response.Response(data)


class UserDetailMedicineAPIVIew(generics.CustomRetrieveAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = UserDetailMedicineSerializer
    queryset = MedicineModel.objects.all().order_by("title")
    object_name = "Medicine"
