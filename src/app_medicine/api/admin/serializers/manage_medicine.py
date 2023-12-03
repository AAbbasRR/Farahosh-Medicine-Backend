from app_medicine.models import MedicineModel

from utils.serializers.serializer import CustomModelSerializer


class AdminListCreateUpdateMedicineSerializer(CustomModelSerializer):
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
            "get_full_name",
        )

    def create(self, validated_data):
        return MedicineModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field_name in validated_data:
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
