from django.urls import path

from .views import *

app_name = "app_medicine_user"
urlpatterns = [
    # medicines
    path(
        "list/pagination/",
        UserListWithPaginationMedicineAPIVIew.as_view(),
        name="list_medicine_with_pagination",
    ),
    path(
        "list/all/",
        UserListAllMedicineAPIVIew.as_view(),
        name="list_medicine_all",
    ),
    path(
        "detail/",
        UserDetailMedicineAPIVIew.as_view(),
        name="detail_medicine",
    ),
]
