from django.urls import path
from .views import register, custom_login, get_user_roles, verify_credentials

urlpatterns = [
    path("login/", custom_login, name="login"),
    path("register/", register, name="register"),
    path("get-user-roles/", get_user_roles, name="get-user-roles"),
    path("verify-credentials/", verify_credentials, name="verify-credentials"),
]


