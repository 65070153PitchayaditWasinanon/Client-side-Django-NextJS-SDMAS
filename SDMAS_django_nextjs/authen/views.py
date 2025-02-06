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