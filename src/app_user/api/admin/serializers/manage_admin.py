from django.db import transaction

from rest_framework import serializers

from app_user.models import UserModel

from utils.serializers.serializer import CustomModelSerializer
from utils.db.validators import PhoneNumberRegexValidator, UniqueValidator


class AdminListAddUpdateAdminSerializer(CustomModelSerializer):
    username = serializers.CharField(
        required=True,
        source="username",
        validators=[UniqueValidator(UserModel.objects.all())],
    )
    mobile_number = serializers.CharField(
        required=True,
        source="mobile_number",
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
            "formatted_last_login",
            "formatted_date_joined",
        )
        extra_kwargs = {"password": {"read_only": True}}

    def serializer_after_access_to_method_and_user(self):
        if self.method == "PUT":
            self.fields["username"].validators = [
                [UniqueValidator(UserModel.objects.exclude(id=self.user.id))]
            ]
            self.fields["mobile_number"].validators = [
                [
                    PhoneNumberRegexValidator,
                    UniqueValidator(UserModel.objects.exclude(id=self.user.id)),
                ]
            ]

    def create(self, validated_data):
        return UserModel.objects.create_superuser(**validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            instance.save()
        return instance
