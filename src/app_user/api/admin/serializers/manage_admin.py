from django.db import transaction

from rest_framework import serializers

from app_user.models import UserModel

from utils.serializers.serializer import CustomModelSerializer
from utils.db.validators import PhoneNumberRegexValidator, UniqueValidator


class AdminListAddUpdateAdminSerializer(CustomModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(UserModel.objects.all())],
    )
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
            "password",
            "first_name",
            "last_name",
            "username",
            "mobile_number",
            "is_staff",
            "is_superuser",
            "formatted_last_login",
            "formatted_date_joined",
        )

    def create(self, validated_data):
        return UserModel.objects.register_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            if password is not None:
                instance.set_password(password)
            instance.save()
        return instance
