from django.urls import path

from authen.views import LoginAPIView, RegisterStudentAPIView, RegisterTechnicianAPIView


urlpatterns = [
    path("api/login/", LoginAPIView.as_view(), name="login2"),
    path("api/register/", RegisterStudentAPIView.as_view(), name="resigter"),
    path("api/register/technician/", RegisterTechnicianAPIView.as_view(), name="resigter"),

]