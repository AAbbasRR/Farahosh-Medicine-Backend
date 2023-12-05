from rest_framework import serializers

from app_user.models import UserModel

from utils.serializers.serializer import CustomModelSerializer
from utils.db.validators import PhoneNumberRegexValidator, UniqueValidator


class AdminListAddUpdateUserSerializer(CustomModelSerializer):
    mobile_number = serializers.CharField(
        required=True,
        validators=[
            PhoneNumberRegexValidator,
            UniqueValidator(UserModel.objects.all()),
        ],
    )

    class Meta:
        model = UserModel
        fields = (
            "id",
            "first_name",
            "last_name",
            "mobile_number",
            "formatted_last_login",
            "formatted_date_joined",
        )

    def create(self, validated_data):
        return UserModel.objects.register_user(
            validated_data["mobile_number"], **validated_data
        )

    def update(self, instance, validated_data):
        for field_name in validated_data:
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
