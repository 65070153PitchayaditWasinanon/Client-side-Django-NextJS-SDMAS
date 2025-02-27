import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User  # หรือโมเดลผู้ใช้ที่คุณใช้
from django.core.mail import send_mail
from django.db.models import Count
from django.http import (
    HttpResponse, 
    JsonResponse, 
    HttpResponseForbidden
)
from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404
)
from django.views import View

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .models import RepairRequest
from .serializers import (
    RepairRequestSerializer, 
    TechnicianRequestSerializer, 
    RepairRequestDjangotoNextJSSerializer, 
    RoomDjangotoNextJSSerializer, 
    RepairAssignmentDjangotoNextJSSerailizer, 
    RequestUpdateDjangotoNextJSSerializer, 
    RepairAssignmentDjangotoNextJSSerializer, 
    TechnicianDjangotoNextJSSerializer, 
    RepairAssignmentCreateSerializer
)



# famnew
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # ต้องผ่านการยืนยันตัวตน (authentication)

    def get(self, request):
        # ดึงข้อมูลของผู้ใช้จาก request.user ซึ่งจะเป็นผู้ที่ล็อกอินอยู่
        user = request.user
        student = getattr(user, 'student', None)  # ดึง Student ถ้ามี
        technician = getattr(user, 'technician', None)  # ดึง Technician ถ้ามี
        room = student.room_id if student else None  # ดึง room_id ถ้าเป็น Student
        # ตัวอย่างข้อมูลที่อาจจะส่งกลับไป
        profile_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "student_id": student.id if student else None,  #  ส่ง student_id ถ้าเป็น Student
            "technician_id": technician.id if technician else None, # ส่ง technician_id ถ้าเป็น Technician
            "room": room.room_number if student else None,
        }

        return Response(profile_data, status=status.HTTP_200_OK)

#famnew
class RepairRequestCreateView(CreateAPIView):
    queryset = RepairRequest.objects.all()  # กำหนด queryset ที่จะใช้
    # ใช้เพื่อระบุว่าเราจะใช้ serializer อะไรในการแปลงข้อมูลจาก JSON ที่ส่งมาจาก client (ในที่นี้คือ React หรือ Postman) ให้เป็น Python object หรือจะใช้ในการแปลง Python object ไปเป็น JSON ที่จะตอบกลับ
    serializer_class = RepairRequestSerializer  # ใช้ serializer ที่เราสร้างขึ้น

    def perform_create(self, serializer):
        # ดึง student ที่เชื่อมโยงกับ user ที่ทำการ request
        
        status = "Reported"
        # บันทึกข้อมูลจาก form data
        serializer.save(status=status)  # จะมีการบันทึกข้อมูลลงฐานข้อมูลพร้อม student ที่เกี่ยวข้อง

    def create(self, request, *args, **kwargs):
        # ใช้ `serializer` เพื่อแปลงข้อมูล JSON ที่มาจาก request.data
        serializer = self.get_serializer(data=request.data)

        # ตรวจสอบความถูกต้องของข้อมูล
        if serializer.is_valid():
            # เรียกใช้ perform_create เพื่อบันทึกข้อมูลลงฐานข้อมูล
            self.perform_create(serializer)
            # ส่งข้อมูลกลับไป
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # หากข้อมูลไม่ถูกต้องจะส่งกลับไปเป็น error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#famedit
class TechnicianRequestCreateView(CreateAPIView):
    queryset = RepairRequest.objects.all()
    serializer_class = TechnicianRequestSerializer

    def perform_create(self, serializer):
        # ดึงค่าจาก request
        repair_request_id = self.request.data.get("repair_request", None)
        technician_id = self.request.data.get("technician", None)

        if isinstance(technician_id, list) and technician_id:
            technician_id = technician_id[0]  # ดึงค่าแรกออกมา

        technician_id = int(technician_id) if technician_id is not None else None

        # ตรวจสอบค่าที่รับเข้ามา
        if not repair_request_id:
            raise ValidationError({"repair_request": "Repair Request ID is required"})

        if not technician_id:
            raise ValidationError({"technician": "Technician ID is required"})

        # ตรวจสอบว่า technician_id มีอยู่จริงหรือไม่
        try:
            technician = Technician.objects.get(id=technician_id)
        except Technician.DoesNotExist:
            raise ValidationError({"technician": "Technician not found"})

        # ตรวจสอบว่า repair_request_id มีอยู่จริงหรือไม่
        try:
            repair_request = RepairRequest.objects.get(id=repair_request_id)
        except RepairRequest.DoesNotExist:
            raise ValidationError({"repair_request": "Repair Request not found"})

        # หา RepairAssignment ที่เกี่ยวข้องกับ repair_request นี้
        repair_request.status = "assigned"
        repair_request.save()
        repair_assignment = RepairAssignment.objects.filter(repair_request=repair_request).first()
        if repair_assignment:
            repair_assignment.technician.remove(technician)  # เอา technician ออกจาก many-to-many

        # บันทึกข้อมูลใหม่
        serializer.save()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Staff - Index Page

class RepairRequestListViewStaff(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repair_requests = RepairRequest.objects.all()  # ดึงข้อมูลทั้งหมด
        serializer = RepairRequestDjangotoNextJSSerializer(repair_requests, many=True)
        return Response(serializer.data)

#Staff - Repair Assign

class RepairAssigmentViewStaffFilteredByID(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        repair_assignment = RepairAssignment.objects.get(repair_request_id=pk) # ดึงข้อมูลทั้งหมด
        serializer = RepairAssignmentDjangotoNextJSSerializer(repair_assignment)
        return Response(serializer.data)

#Staff - AssignJob Filter By ID

class RepairRequestFilteredbyIDViewStaff(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            repair_request = RepairRequest.objects.get(id=id)
            serializer = RepairRequestDjangotoNextJSSerializer(repair_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RepairRequest.DoesNotExist:
            return Response({"error": "Repair request not found"}, status=status.HTTP_404_NOT_FOUND)

class TechnicianViewStaffAssignJob(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            technician = Technician.objects.all()
            serializer = TechnicianDjangotoNextJSSerializer(technician, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Technician.DoesNotExist:
            return Response({"error": "Repair request not found"}, status=status.HTTP_404_NOT_FOUND)

class StaffAssignCreateView(CreateAPIView):
    # ใช้เพื่อระบุว่าเราจะใช้ serializer อะไรในการแปลงข้อมูลจาก JSON ที่ส่งมาจาก client (ในที่นี้คือ React หรือ Postman) ให้เป็น Python object หรือจะใช้ในการแปลง Python object ไปเป็น JSON ที่จะตอบกลับ
    serializer_class = RepairAssignmentCreateSerializer  # ใช้ serializer ที่เราสร้างขึ้น

    def perform_create(self, serializer):
        # ดึง student ที่เชื่อมโยงกับ user ที่ทำการ request
        
        # บันทึกข้อมูลจาก form data
        # serializer.save()  # จะมีการบันทึกข้อมูลลงฐานข้อมูลพร้อม student ที่เกี่ยวข้อง
        repair_assignment = serializer.save()
        repair_assignment.technician.set(serializer.validated_data["technician"])

    def create(self, request, *args, **kwargs):
        # ใช้ `serializer` เพื่อแปลงข้อมูล JSON ที่มาจาก request.data
        serializer = self.get_serializer(data=request.data)

        # ตรวจสอบความถูกต้องของข้อมูล
        if serializer.is_valid():
            # เรียกใช้ perform_create เพื่อบันทึกข้อมูลลงฐานข้อมูล
            self.perform_create(serializer)
            # ส่งข้อมูลกลับไป
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # หากข้อมูลไม่ถูกต้องจะส่งกลับไปเป็น error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffAssignEditView(APIView):
    def put(self, request, pk, *args, **kwargs):
        # ดึงข้อมูล RepairAssignment ตามค่า pk ที่ได้รับ
        repair_assignment = get_object_or_404(RepairAssignment, repair_request_id=pk)
        
        # ทำการ validate และอัพเดตข้อมูลด้วย serializer
        serializer = RepairAssignmentCreateSerializer(repair_assignment, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_assignment = serializer.save()
            
            # อัพเดต technician ที่เชื่อมโยง (M2M field)
            if "technician" in serializer.validated_data:
                new_technicians = serializer.validated_data["technician"]

                # ใช้ add() เพื่อเพิ่มช่างใหม่เข้าไปโดยไม่ลบของเดิม
                updated_assignment.technician.add(*new_technicians)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#update-famf
class TechnicianRepairUpdateView(CreateAPIView):
    def post(self, request):
        repair_update_id = request.data.get('id')
        status1 = request.data.get('status')
        repair_update_id = int(repair_update_id)

        repairstatusupdate = get_object_or_404(RepairStatusUpdate, id=repair_update_id)
        repairassignment = get_object_or_404(RepairAssignment, repair_request__id = repairstatusupdate.repair_request.id)
        repairrequest = get_object_or_404(RepairRequest, id=repairstatusupdate.repair_request.id)

        if status1.lower() == "completed":
            if repairassignment:
                repairassignment.technician.clear()  # ลบ Technician ที่เชื่อมอยู่
                repairassignment.delete()  # ลบ RepairAssignment เอง
            repairstatusupdate.delete()
            repairrequest.delete()
        else:
            repairstatusupdate.status = status1
            repairstatusupdate.save()
    
            repairrequest.status = status1
            repairrequest.save()

            if repairassignment:
                repairassignment.status = status1  # ต้องแน่ใจว่า RepairAssignment มี status จริงๆ
                repairassignment.save()

        return Response({
            "message": "Repair request updated successfully",
            "id": repair_update_id,
            "status": status1,
        },status=status.HTTP_200_OK)

#famnew
class RepairRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_id = request.query_params.get("student_id", None)
        
        if not student_id:
            return Response({"error": "Missing student_id"}, status=400)

        try:
            student = Student.objects.get(id=student_id, user=request.user)
            repair_requests = RepairRequest.objects.filter(student=student)
            serializer = RepairRequestDjangotoNextJSSerializer(repair_requests, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        
    def delete(self, request, repair_request_id):
        """
        ลบ RepairRequest โดยต้องเป็นเจ้าของเท่านั้น
        """
        repair_request = get_object_or_404(RepairRequest, id=repair_request_id)

        # ตรวจสอบว่า repair_request เป็นของ student นี้หรือไม่
        if repair_request.student.user != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        repair_request.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
#famnew
class RepairUpdateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            repair_update = RepairStatusUpdate.objects.get(id=id)
            serializer = RequestUpdateDjangotoNextJSSerializer(repair_update)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RepairRequest.DoesNotExist:
            return Response({"error": "Repair request not found"}, status=status.HTTP_404_NOT_FOUND)

# fam
class StudentTrackstatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_id = request.query_params.get("student_id", None)
        
        if not student_id:
            return Response({"error": "Missing student_id"}, status=400)
        
        try:
            student = Student.objects.get(id=student_id, user=request.user)
            repair_requests = RepairRequest.objects.filter(student=student)
            #  ทำให้ Django ค้นหาทุก RepairStatusUpdate ที่ repair_request อยู่ในรายการ repair_requests
            requests_update = RepairStatusUpdate.objects.filter(repair_request__in=repair_requests)
            serializer = RequestUpdateDjangotoNextJSSerializer(requests_update, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

#fam
class RepairAssignmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        technician_id = request.query_params.get("technician_id", None)
        
        if not technician_id:
            return Response({"error": "Missing student_id"}, status=400)
        
        try:
            technician = Technician.objects.get(id=technician_id, user=request.user)
            repair_assignmen = RepairAssignment.objects.filter(technician=technician)
            serializer = RepairAssignmentDjangotoNextJSSerializer(repair_assignmen, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

#famnew
class RepairStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        technician_id = request.query_params.get("technician_id", None)
        
        if not technician_id:
            return Response({"error": "Missing student_id"}, status=400)
        
        try:
            technician = Technician.objects.get(id=technician_id, user=request.user)
            repair_statusupdate = RepairStatusUpdate.objects.filter(technician=technician)

            serializer = RequestUpdateDjangotoNextJSSerializer(repair_statusupdate, many=True)
            return Response(serializer.data)
        
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

#famnew
class RepairRequestFilteredbyIDView(APIView):
    def get(self, request, id):
        try:
            repair_request = RepairRequest.objects.get(id=id)
            
            serializer = RepairRequestDjangotoNextJSSerializer(repair_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RepairRequest.DoesNotExist:
            return Response({"error": "Repair request not found"}, status=status.HTTP_404_NOT_FOUND)

#famnew
class RepairRequestEditFilteredbyIDView(APIView):
    def post(self, request):
        repair_request_id = request.data.get('repair_request_id')
        student = request.data.get('student')
        description = request.data.get('description')
        urgency = request.data.get('urgency')
        repair_appointment_time = request.data.get('repair_appointment_time')

        print(f"Received repair_request_id: {repair_request_id}")
        print(f"Received student: {student}")

        if not all([repair_request_id, student, description, urgency, repair_appointment_time]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        repair_request = get_object_or_404(RepairRequest, id=repair_request_id)

        try:
            repair_request.student_id = int(student) if student else None
            repair_request.description = description
            repair_request.urgency = urgency
            repair_request.repair_appointment_time = repair_appointment_time
            repair_request.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "Repair request updated successfully",
            "id": repair_request_id,
            "student": student,
            "description": description,
            "urgency": urgency,
            "repair_appointment_time": repair_appointment_time,
        }, status=status.HTTP_200_OK)

class RepairASsignmentFilterbyIDTechnicianView(APIView):
    def get(self, request, id):
        try:
            repair_assignment = RepairAssignment.objects.filter(technician=id)
            serializer = RepairAssignmentDjangotoNextJSSerailizer(repair_assignment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RepairAssignment.DoesNotExist:
            return Response({"error": "Repair request not found"}, status=status.HTTP_404_NOT_FOUND)

# fam
class RoomView(APIView):
    def get(self, request):
        room = Room.objects.all()
        serializer = RoomDjangotoNextJSSerializer(room, many=True)
        return Response(serializer.data) #ส่งข้อมูลไปเป็น json
