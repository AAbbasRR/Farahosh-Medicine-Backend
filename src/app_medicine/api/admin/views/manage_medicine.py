from app_medicine.api.admin.serializers.manage_medicine import (
    AdminListCreateUpdateMedicineSerializer,
)
from app_medicine.models import MedicineModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.paginations import BasePagination
from utils.views.permissions import IsAdminUserPermission, IsAuthenticatedPermission


class AdminListCreateMedicineAPIVIew(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminListCreateUpdateMedicineSerializer
    search_fields = ["brand_code", "title", "shape", "dose"]
    queryset = MedicineModel.objects.all().order_by("title")


class AdminUpdateDeleteMedicineAPIVIew(generics.CustomUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminListCreateUpdateMedicineSerializer
    queryset = MedicineModel.objects.all().order_by("title")
    object_name = "Medicine"
