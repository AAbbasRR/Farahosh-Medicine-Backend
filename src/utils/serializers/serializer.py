from rest_framework import serializers

from utils.functions import get_client_ip
from utils.exceptions.rest import NotFoundObjectException


class CustomSerializer(serializers.Serializer):
    exclude_required_fields_for_update = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request", None)
        if self.request:
            self.serializer_have_request_on_context(*args, **kwargs)
            self.user = self.request.user
            self.method = self.request.method
            self.serializer_after_access_to_method_and_user(*args, **kwargs)

    def serializer_have_request_on_context(self, *args, **kwargs):
        pass

    def serializer_after_access_to_method_and_user(self, *args, **kwargs):
        pass

    @property
    def client_ip(self):
        if self.request:
            return get_client_ip(self.request)
        else:
            return None


class CustomModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.request = self.context.get("request", None)
        if self.request:
            self.serializer_have_request_on_context(*args, **kwargs)
            self.user = self.request.user
            self.method = self.request.method
            self.serializer_after_access_to_method_and_user(*args, **kwargs)
            if self.method in ["PUT"]:
                exclude_required_fields_for_update = getattr(
                    self.Meta, "exclude_required_fields_for_update", ()
                )
                for field_name, field in self.fields.items():
                    if field_name not in exclude_required_fields_for_update:
                        field.required = False

    def serializer_have_request_on_context(self, *args, **kwargs):
        pass

    def serializer_after_access_to_method_and_user(self, *args, **kwargs):
        pass

    def get_find_object(self, model, pk, object_name=None, allow_null=False):
        if allow_null:
            if pk is None:
                return None
        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise NotFoundObjectException(
                object_name=object_name if object_name is not None else model.__name__
            )

    @property
    def client_ip(self):
        if self.request:
            return get_client_ip(self.request)
        else:
            return None
