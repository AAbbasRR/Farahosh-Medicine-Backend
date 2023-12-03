from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from utils.serializers.serializer import CustomSerializer
from utils.exceptions.rest import OldPasswordIsIncorrectException
from utils.base_errors import BaseErrors


class AdminChangePasswordSerializer(CustomSerializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
    )
    new_re_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate_old_password(self, value):
        if not self.user.check_password(value):
            raise OldPasswordIsIncorrectException()
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_re_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": [BaseErrors.passwords_do_not_match],
                    "new_re_password": [BaseErrors.passwords_do_not_match],
                }
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance
