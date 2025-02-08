from django.urls import path
# from .views import RegisterView, LoginView

from . import views

urlpatterns = [
    path('', views.RedirectView.as_view(), name='redirect'),
    # /index_form/
    path("repair/", views.StudentRepairRequestView.as_view(), name="index"),

    path("trackstatus/", views.TrackStatusView.as_view(), name="trackstatus"),

    path("student/trackstatus/", views.StudentTrackStatusView.as_view(), name="student-trackstatus"),

    path("deletestatus/<int:pk>/", views.DeleteStatusView.as_view(), name="deletestatus"),

    path("trackstatus/<int:pk>/", views.EditDetailView.as_view(), name="trackstatus-detail"),

    path("staff/", views.StaffView.as_view(), name="staff"),

    path("staff/assign/detail/<int:pk>/", views.StaffAssignDetailView.as_view(), name="staffassigndetail"),

    path("staff/assign/edit/<int:pk>/", views.StaffAssignEditView.as_view(), name="staffassignedit"),

    path("staff/delete/<int:pk>/<int:tech_id>", views.DeleteTechnicianAssignView.as_view(), name="deletetechassign"),

    path("staff/manage/student/", views.StaffManageStudentView.as_view(), name="managestudent"),

    path("staff/manage/student/edit/<int:pk>/", views.StaffManageEditStudentView.as_view(), name="editstudent"),

    path("staff/manage/student/delete/<int:pk>/", views.StaffManageDeleteStudentView.as_view(), name="deletestudent"),

    path("staff/manage/technician/", views.StaffManageTechnicianView.as_view(), name="managetechnician"),

    path("staff/manage/technician/edit/<int:pk>/", views.StaffManageEditTechnicianView.as_view(), name="edittechnician"),

    path("staff/manage/technician/delete/<int:pk>/", views.StaffManageDeleteTechnicianView.as_view(), name="deletetechnician"),

    path("staff/history/", views.StaffHistoryView.as_view(), name="history"),

    path("staff/room/", views.StaffRoomView.as_view(), name="room"),

    path("staff/room/add/", views.StaffAddRoomView.as_view(), name="addroom"),

    path("staff/room/edit/<int:pk>/", views.StaffEditRoomView.as_view(), name="editroom"),

    path("staff/room/delete/<int:pk>/", views.StaffDeleteRoomView.as_view(), name="deleteroom"),

    path("technician/", views.TechnicianView.as_view(), name="technician"),

    path("technicianedit/", views.TechnicianEditView.as_view(), name="technicianedit"),

    path("technician/detail/<int:pk>/", views.TechnicainDetailView.as_view(), name="technician-detail"),

    path("technician/update/<int:pk>/", views.TechnicainUpdateView.as_view(), name="technician-update"),

    path('api/repair-requests/', views.RepairRequestCreateView.as_view(), name='repair-request-create'),

    path('api/repair-requests-views/', views.RepairRequestListView.as_view(), name='repair-request-view'),
    
    path('api/technician-requests/', views.TechnicianRequestCreateView.as_view(), name='technician-request-create'),

    path('api/profile/', views.ProfileView.as_view(), name='profile'),

    # path('api/register/', views.RegisterView.as_view(), name='register'),

    # path('api/login/', views.LoginView.as_view(), name='login'),
    # # /employee/position/
    # path("position/", views.PositionView.as_view(), name="position"),
    # # /employee/project
    # path("project/", views.ProjectView.as_view(), name="project"),
    # # /employee/project/num
    # path("project/<int:pro_id>/", views.ProjectView.as_view(), name="project-delete"),
    # #/project_id/project_details
    # path("details/<int:project_id>/", views.ProjectDetailView.as_view(), name="details"),
    # #/project_id/project_details/staff_id
    # path("details/<int:project_id>/<int:staff_id>/", views.ProjectDetailView.as_view(), name="details_staff_add"),
    # path("details/<int:project_id>/<int:staff_id>/", views.ProjectDetailView.as_view(), name="details_staff_add"),
    # #/project/form/
    # path("project/form/", views.ProjectFormView.as_view(), name="project_form"),
    # #/project/form/
    # path("employee/form/", views.EmployeeFormView.as_view(), name="employee_form"),
    #  #/project_id/project_details/form
    # path("details/<int:project_id>/form", views.UpdateProjectDetailView.as_view(), name="projectdetail_form"),
]