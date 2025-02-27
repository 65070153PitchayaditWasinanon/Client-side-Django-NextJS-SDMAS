from django.urls import path
# from .views import RegisterView, LoginView

from . import views

urlpatterns = [
    #famnew
    path('api/repair-requests/', views.RepairRequestCreateView.as_view(), name='repair-request-create'),

    #famnew
    path('api/repair-requests-update-get/<int:id>/', views.RepairUpdateListView.as_view(), name='repair-update-get'),

    #famnew
    path('api/repair-requests-views/', views.RepairRequestListView.as_view(), name='repair-request-view'),

    path('api/repair-requests-views-staff/', views.RepairRequestListViewStaff.as_view(), name='repair-request-view-staff'),

    path('api/staff/technician/', views.TechnicianViewStaffAssignJob.as_view(), name='staff-get-technician-for-assign-job'),

    path('api/staff-edit-repairassignment/<int:pk>/', views.StaffAssignEditView.as_view(), name='staff-edit-repairassignment'),

    path('api/staff/assignment/technician/<int:pk>/', views.RepairAssigmentViewStaffFilteredByID.as_view(), name='staff-edit-technician-show'),

    path('api/staff-create-repairassignment/', views.StaffAssignCreateView.as_view(), name='staff-create-repairassignment'),

    path('api/repair-requests-staff/<int:id>/', views.RepairRequestFilteredbyIDViewStaff.as_view(), name='repair_request_detail-staff'),

    #famnew
    path('api/repair-requests-views/<int:repair_request_id>/', views.RepairRequestListView.as_view(), name='delete-repair-request'),
    
    #famnew
    path('api/student-trackstatus-views/', views.StudentTrackstatusView.as_view(), name='student-trackstatus-view'),
    
    #famnew
    path('api/requests-asignment-views/', views.RepairAssignmentView.as_view(), name='requests-asignment-views'),

    #famnew
    path('api/repair-status-update-views/', views.RepairStatusUpdateView.as_view(), name='repair-status-update-views'),

    #famnew
    path('api/repair-requests/<int:id>/', views.RepairRequestFilteredbyIDView.as_view(), name='repair_request_detail'),

    #famnew
    path('api/repair-requests-edit/', views.RepairRequestEditFilteredbyIDView.as_view(), name='repair_request_edit_detail'),

    path('api/repair-assignment-filter/<int:id>/', views.RepairASsignmentFilterbyIDTechnicianView.as_view(), name='repair_assignment_filter_by_techinician_id'),
    
    #famnew
    path('api/technician-requests/', views.TechnicianRequestCreateView.as_view(), name='technician-request-create'),

    #famnew
    path('api/technician-repair-update/', views.TechnicianRepairUpdateView.as_view(), name='technician-repair-updateView'),

    #famnew
    path('api/profile/', views.ProfileView.as_view(), name='profile'),

    # fam
    path('api/room/', views.RoomView.as_view(), name='room-view'),
]
