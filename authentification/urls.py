from django.urls import path
from .views import register_user,login_user , check_auth , logout_view , get_user_info

urlpatterns = [
    path("register/", register_user , name="register"),
    path("login/", login_user , name="login"),
    path("check/", check_auth , name="check"),
    path("info/" , get_user_info , name="info"),
    path("logout/", logout_view , name="logout"),
]
