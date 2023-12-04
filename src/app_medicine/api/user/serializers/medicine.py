from app_medicine.models import MedicineModel

from utils.serializers.serializer import CustomModelSerializer


class UserListMedicineSerializer(CustomModelSerializer):
    class Meta:
        model = MedicineModel
        fields = (
            "id",
            "brand_code",
            "title",
            "shape",
            "dose",
            "price_exchange_subsidy",
        )


class UserDetailMedicineSerializer(CustomModelSerializer):
    class Meta:
        model = MedicineModel
        fields = (
            "id",
            "brand_code",
            "title",
            "term",
            "shape",
            "dose",
            "price_exchange_subsidy",
            "percent_share_of_organization_exchange_subsidy",
            "price_of_percent_organization",
        )
