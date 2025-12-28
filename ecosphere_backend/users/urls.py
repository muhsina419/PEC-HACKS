from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import PhoneTokenObtainPairView, ProfileView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", PhoneTokenObtainPairView.as_view(), name="login"),
    path("token/", PhoneTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
