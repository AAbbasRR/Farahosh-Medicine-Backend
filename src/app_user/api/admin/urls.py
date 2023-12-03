from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

app_name = "app_user_admin"
urlpatterns = [
    # login
    path("login/", AdminLoginAPIView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_token_refresh"),
    # info
    path("info/", AdminInfoAPIView.as_view(), name="info_account"),
    # change password
    path(
        "change_password/", AdminChangePasswordAPIView.as_view(), name="change_password"
    ),
    # manage normal users
    path(
        "manage/user/list_create/",
        AdminListCreateUserAPIView.as_view(),
        name="list_create_manage_user",
    ),
    path(
        "manage/user/update_delete/",
        AdminUpdateDeleteUserAPIView.as_view(),
        name="update_delete_manage_user",
    ),
    # manage admin users
    path(
        "manage/admin/list_create/",
        AdminListCreateAdminAPIView.as_view(),
        name="list_create_manage_admin",
    ),
    path(
        "manage/admin/update_delete/",
        AdminUpdateDeleteAdminAPIView.as_view(),
        name="update_delete_manage_admin",
    ),
]
