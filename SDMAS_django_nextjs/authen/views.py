from django.contrib.auth import (
    authenticate, 
    login, 
    logout
)
from django.contrib.auth.forms import (
    AuthenticationForm, 
    PasswordChangeForm
)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404
)
from django.views import View
from django.views.generic import FormView

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from SDMAS.models import *


class RegisterTechnicianAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        
        technician_id = request.data.get('technician_id')
        expertise = request.data.get('expertise')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not technician_id or not expertise:
            return Response({"error": "Technician ID and expertise are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        # สร้างผู้ใช้ใหม่
        user = User.objects.create(
            username=username,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
        )
        technician = Technician.objects.create(user=user, technician_id=technician_id, expertise=expertise)
        technician.save()

        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)

class RegisterStudentAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        room_number = request.data.get('room_number')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # สร้างผู้ใช้ใหม่
        user = User.objects.create(
            username=username,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
        )
        # ValueRoom = Room.objects.get(room_number = room_number)
        room = get_object_or_404(Room, room_number=room_number)

        # เช็คว่าเป็นผู้ใช้ประเภทไหน (Student หรือ Technician)
        
        student = Student.objects.create(user=user, room_id=room)
        student.save()

        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            role = user.groups.first().name if user.groups.exists() else "User" #เพิ่มเข้ามา 19/2/2568 23:01 เนื่องจากต้องการให้ staff login แล้วผ่าน IsAuthenticated
            
            # getattr(user, 'student', None): ถ้า user มี student ซึ่งหมายถึงว่า user นี้มีความสัมพันธ์กับ Student model, เช่น User นี้เชื่อมต่อกับโมเดล Student ผ่าน OneToOneField
            student = getattr(user, 'student', None)  # ดึง Student ถ้ามี
            technician = getattr(user, 'technician', None)  # ดึง Technician ถ้ามี
            # staff = role == "staff"  # ตรวจสอบว่าผู้ใช้เป็น Staff หรือไม่ เพิ่มเข้ามา 19/2/2568 23:01 เนื่องจากต้องการให้ staff login แล้วผ่าน IsAuthenticated

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.groups.first().name if user.groups.exists() else "User"
                },
                "student_id": student.id if student else None,  # ส่ง student_id ถ้าเป็น Student
                "technician_id": technician.id if technician else None,  # ส่ง technician_id ถ้าเป็น Technician
                # "is_staff": staff.id if technician else None # ส่งค่า is_staff กลับไป เพิ่มเข้ามา 19/2/2568 23:01 เนื่องจากต้องการให้ staff login แล้วผ่าน IsAuthenticated
            })
        return Response({"error": "Invalid credentials"}, status=400)