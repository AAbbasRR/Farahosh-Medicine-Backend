from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

app_name = "app_user_user"
urlpatterns = [
    # login
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("login/verify/", UserVerifyLoginOtpAPIView.as_view(), name="verify_login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_token_refresh"),
    # info
    path("info/", UserInfoAPIView.as_view(), name="info_account"),
]
