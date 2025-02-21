from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import RegisterForm, RegisterForm2
from SDMAS.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from SDMAS.models import Student

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from django.shortcuts import get_object_or_404

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

        if not technician_id or not expertise:  # ✅ เพิ่มเงื่อนไขกัน error
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
        # ValueRoom = Room.objects.get(room_number = room_number)
        # room = get_object_or_404(Room, room_number=room_number)

        # เช็คว่าเป็นผู้ใช้ประเภทไหน (Student หรือ Technician)
        
        # student = Student.objects.create(user=user, room_id=room)
        # student.save()
        
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
        
        # Technician.objects.create(user=user, technician_id="T" + str(user.id), expertise="General")  # ปรับได้ตามต้องการ

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
            
            # ✅ ตรวจสอบว่าผู้ใช้เป็น Student หรือ Technician
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
                "student_id": student.id if student else None,  # ✅ ส่ง student_id ถ้าเป็น Student
                "technician_id": technician.id if technician else None,  # ✅ ส่ง technician_id ถ้าเป็น Technician
                # "is_staff": staff.id if technician else None # ✅ ส่งค่า is_staff กลับไป เพิ่มเข้ามา 19/2/2568 23:01 เนื่องจากต้องการให้ staff login แล้วผ่าน IsAuthenticated
            })
        return Response({"error": "Invalid credentials"}, status=400)


# class LoginView2(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)  # Django login session
#             student = Student.objects.get(user=user)
#             return Response({"message": "Login successful", "student_id": student.id}, status=200)

#         return Response({"error": "Invalid credentials"}, status=400)


class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if user.groups.filter(name="Student").exists():
                return redirect('index')
            elif user.groups.filter(name="Technician").exists():
                return redirect("technician")
            elif user.groups.filter(name="Staff").exists():
                return redirect("staff")

        return render(request,'login.html', {"form":form})


class LogoutView(LoginRequiredMixin, View):
    login_url = '/auth/'

    def get(self, request):
        logout(request)
        return redirect('login')
    
class RegisterView(FormView):

    def get(self, request):
        form = RegisterForm()
        #   # เปลี่ยนเส้นทางไปที่หน้า Login หลังจากสมัครเสร็จ
        return render(request, 'register.html', {"form": form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # บันทึกข้อมูลผู้ใช้
            room_id = form.cleaned_data.get('room_id')

            # สร้าง Student object เชื่อมกับ User และ Room ที่เลือก
            student = Student.objects.create(user=user, room_id=room_id)
            student.save()
            
            # หลังจากสมัครเสร็จแล้วเข้าสู่ระบบให้ผู้ใช้
            # login(self.request, user)

            return redirect('login')
        return render(request, 'register.html', {"form": form})
    
class RegisterTechnicianView(FormView):

    def get(self, request):
        form = RegisterForm2()
        return render(request, 'register-tecnician.html', {"form": form})

    def post(self, request):
        form = RegisterForm2(request.POST)
        
        if form.is_valid():  # ตรวจสอบว่าฟอร์มถูกต้องหรือไม่
            user = form.save()  # บันทึกข้อมูลผู้ใช้
            technician_id = form.cleaned_data['technician_id']
            expertise = form.cleaned_data['expertise']

            # สร้าง Technician object เชื่อมกับ User ที่เลือก
            technician = Technician.objects.create(user=user, technician_id=technician_id, expertise=expertise)
            technician.save()
            
            # หลังจากสมัครเสร็จแล้วเข้าสู่ระบบให้ผู้ใช้
            login(request, user)

            return redirect('login')  # เปลี่ยนเส้นทางไปยังหน้า Login หลังจากสมัครเสร็จ

        # ถ้าฟอร์มไม่ถูกต้องให้แสดงฟอร์มพร้อม error message
        return render(request, 'register-tecnician.html', {"form": form})

class ChangePasswordView(LoginRequiredMixin, FormView):
    login_url = '/auth/'

    def get(self, request):
        userprofile = request.user
        form = PasswordChangeForm(userprofile)
        return render(request, 'change-password.html', {"form": form})
    
    def post(self, request):
        userprofile = request.user
        form = PasswordChangeForm(userprofile, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            return redirect('login')
        else:
            print(form.errors)
            return render(request, 'change-password.html', {"form": form})