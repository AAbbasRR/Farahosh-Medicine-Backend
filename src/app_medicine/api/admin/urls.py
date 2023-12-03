from django.urls import path

from .views import *

app_name = "app_medicine_admin"
urlpatterns = [
    # manage medicine
    path(
        "manage/list_create/",
        AdminListCreateMedicineAPIVIew.as_view(),
        name="list_create_manage_medicine",
    ),
    path(
        "manage/update_delete/",
        AdminUpdateDeleteMedicineAPIVIew.as_view(),
        name="update_delete_manage_medicine",
    ),
]
