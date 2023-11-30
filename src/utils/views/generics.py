from django.shortcuts import get_object_or_404
from django.http.response import Http404

from rest_framework import (
    generics,
    status,
    response,
)

from utils.exceptions.rest import (
    NotFoundObjectException,
    ParameterRequiredException,
)


class CustomListAPIView(generics.ListAPIView):
    pass


class CustomListCreateAPIView(generics.ListCreateAPIView):
    pass


class CustomCreateAPIView(generics.CreateAPIView):
    pass


class CustomRetrieveAPIView(generics.RetrieveAPIView):
    lookup_fields = [
        "pk",
    ]
    object_name = ""

    def get_object(self):
        param_error = False
        filter = {}
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field, None)
            if param_value is None or param_value == "":
                param_error = True
            else:
                filter[lookup_field] = param_value
                param_error = False
                break
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, **filter)
            return obj
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    http_method_names = [
        "get",
        "put",
        "head",
        "options",
    ]
    lookup_fields = [
        "pk",
    ]
    object_name = ""

    def get_object(self):
        param_error = False
        filter = {}
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field, None)
            if param_value is None or param_value == "":
                param_error = True
            else:
                filter[lookup_field] = param_value
                param_error = False
                break
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, **filter)
            return obj
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    lookup_fields = [
        "pk",
    ]
    object_name = ""

    def get_object(self):
        param_error = False
        filter = {}
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field, None)
            if param_value is None or param_value == "":
                param_error = True
            else:
                filter[lookup_field] = param_value
                param_error = False
                break
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, **filter)
            return obj
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = [
        "get",
        "put",
        "delete",
        "head",
        "options",
    ]
    lookup_fields = [
        "pk",
    ]
    object_name = ""

    def get_object(self):
        param_error = False
        filter = {}
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field, None)
            if param_value is None or param_value == "":
                param_error = True
            else:
                filter[lookup_field] = param_value
                param_error = False
                break
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, **filter)
            return obj
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomUpdateAPIView(generics.UpdateAPIView):
    lookup_fields = [
        "pk",
    ]
    object_name = ""

    def get_object(self):
        param_error = False
        filter = {}
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field, None)
            if param_value is None or param_value == "":
                param_error = True
            else:
                filter[lookup_field] = param_value
                param_error = False
                break
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, **filter)
            return obj
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomDestroyAPIView(generics.DestroyAPIView):
    lookup_fields = [
        "pk",
    ]
    object_name = ""

    def get_object(self):
        param_error = False
        filter = {}
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field, None)
            if param_value is None or param_value == "":
                param_error = True
            else:
                filter[lookup_field] = param_value
                param_error = False
                break
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, **filter)
            return obj
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = [
        "put",
        "delete",
        "head",
        "options",
    ]
    lookup_fields = [
        "pk",
    ]
    object_name = ""

    def get_object(self):
        param_error = False
        filter = {}
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field, None)
            if param_value is None or param_value == "":
                param_error = True
            else:
                filter[lookup_field] = param_value
                param_error = False
                break
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, **filter)
            return obj
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomGenericAPIView(generics.GenericAPIView):
    pass


class CustomGenericPostAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=self.request.data)
        if ser.is_valid(raise_exception=True):
            return response.Response(ser.validated_data, status=status.HTTP_200_OK)


class CustomGenericGetAPIView(generics.GenericAPIView):
    serializable_object = None

    def get_serializable_object(self):
        return self.serializable_object

    def get(self, *args, **kwargs):
        ser = self.get_serializer(self.get_serializable_object())
        return response.Response(ser.data)
