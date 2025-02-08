from django.urls import path

from authen.views import LoginView, LogoutView, RegisterView, RegisterTechnicianView, ChangePasswordView,LoginAPIView


urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/technician/', RegisterTechnicianView.as_view(), name='register-tecnician'),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),

    # path('api/login/', LoginView2.as_view(), name='login2'),
    path("api/login/", LoginAPIView.as_view(), name="login2"),
]