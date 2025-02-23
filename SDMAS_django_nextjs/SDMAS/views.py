from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
import json
from django.http import JsonResponse, HttpResponseForbidden
from SDMAS.forms import RepairRequestForm, StaffAssignmentForm, TechnicainAssignmentForm, StudentInfoForm, TechnicainUpdateForm, TechnicianInfoForm, RoomAddForm
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.conf import settings
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import RepairRequest
from .serializers import RepairRequestSerializer, TechnicianRequestSerializer
from .serializers import RepairRequestSerializer, RepairRequestDjangotoNextJSSerializer, RoomDjangotoNextJSSerializer, RepairAssignmentDjangotoNextJSSerailizer, RequestUpdateDjangotoNextJSSerializer, RepairAssignmentDjangotoNextJSSerializer, TechnicianDjangotoNextJSSerializer, RepairAssignmentCreateSerializer

from rest_framework.views import APIView

# ใน views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User  # หรือโมเดลผู้ใช้ที่คุณใช้
from rest_framework.exceptions import ValidationError


# fam
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
            "student_id": student.id if student else None,  # ✅ ส่ง student_id ถ้าเป็น Student
            "technician_id": technician.id if technician else None, # ✅ ส่ง technician_id ถ้าเป็น Technician
            "room": room.room_number if student else None,
        }

        return Response(profile_data, status=status.HTTP_200_OK)


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffAssignCreateView(CreateAPIView):
    # queryset = RepairAssignment.objects.all()  # กำหนด queryset ที่จะใช้
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
#update-famf
class TechnicianRepairUpdateView(CreateAPIView):
    def post(self, request):
        repair_update_id = request.data.get('id')
        status1 = request.data.get('status')
        repair_update_id = int(repair_update_id)
        # description = request.data.get('description')
        # urgency = request.data.get('urgency')
        # repair_appointment_time = request.data.get('repair_appointment_time')

        # print(f"Received repair_request_id: {repair_request_id}")
        # print(f"Received student: {student}")

        # if not all([repair_request_id, student, description, urgency, repair_appointment_time]):
        #     return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        repairstatusupdate = get_object_or_404(RepairStatusUpdate, id=repair_update_id)
        repairrequest = get_object_or_404(RepairRequest, id=repairstatusupdate.repair_request.id)


        if status1 == "completed":
            repairstatusupdate.delete()
            repairrequest.delete()
        else:
            repairstatusupdate.status = status1
            repairstatusupdate.save()
        # try:
        #     repairstatusupdate.status = status
            
        #     repairstatusupdate.save()
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "Repair request updated successfully",
            "id": repair_update_id,
            "status": status1,
        },status=status.HTTP_200_OK)
    # queryset = RepairRequest.objects.all()
    # serializer_class = TechnicianRequestSerializer  

    # def perform_create(self, serializer):
    #     # ดึงค่าจาก request
    #     repair_update_id = self.request.data.get("id", None)
    #     status = self.request.data.get("status", None)
    #     technician_id = self.request.data.get("technician", None)

    #     if isinstance(technician_id, list) and technician_id:  
    #         technician_id = technician_id[0]  # ดึงค่าแรกออกมา

    #     technician_id = int(technician_id) if technician_id is not None else None

    #     if not repair_update_id:
    #         raise ValidationError({"id": "Repair Update ID is required"})

    #     # ตรวจสอบค่าที่รับเข้ามา
    #     # if not repair_request_id:
    #     #     raise ValidationError({"repair_request": "Repair Request ID is required"})

    #     if not technician_id:
    #         raise ValidationError({"technician": "Technician ID is required"})

    #     # ตรวจสอบว่า technician_id มีอยู่จริงหรือไม่
    #     try:
    #         technician = Technician.objects.get(id=technician_id)
    #     except Technician.DoesNotExist:
    #         raise ValidationError({"technician": "Technician not found"})

    #     # ตรวจสอบว่า repair_request_id มีอยู่จริงหรือไม่
    #     try:
    #         repair_update = RepairStatusUpdate.objects.get(id=repair_update_id)
    #     except RepairStatusUpdate.DoesNotExist:
    #         raise ValidationError({"repair_request": "Repair Request not found"})

    #     # หา RepairAssignment ที่เกี่ยวข้องกับ repair_request นี้
    #     if status == "completed":
    #         repair_update.delete()
    #     else:
    #         repair_update.status = status
    #         repair_update.save()
        

    #     # บันทึกข้อมูลใหม่
    #     serializer.save()

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRepairRequestView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.add_repairrequest"]

    def get(self, request):
        student_target = Student.objects.get(user__id = request.user.id)
        form = RepairRequestForm()
        return render(request, 'index.html', {"form":form, "student_target": student_target})
    
    def post(self, request):
        student_target = Student.objects.get(user__id = request.user.id)
         # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = RepairRequestForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                description = form.cleaned_data["description"]
                urgency = form.cleaned_data["urgency"]
                repair_appointment_time = form.cleaned_data["repair_appointment_time"]

                student = Student.objects.get(user__id = request.user.id)

                request_create = RepairRequest.objects.create(
                    student = student, 
                    description = description,
                    urgency = urgency,
                    repair_appointment_time = repair_appointment_time,
                    status = "Reported"
                )
                request_create.save()

                return redirect("trackstatus")
            else:
                return render(request, 'index.html', {"form":form, "student_target": student_target})
            
#fam
class TrackStatusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    #LoginRequiredMixin Mixin ที่ใช้บังคับว่าผู้ใช้ต้องเข้าสู่ระบบก่อน จึงจะเข้าถึง View นี้ได้ หากยังไม่ได้เข้าสู่ระบบ จะถูกเปลี่ยนเส้นทางไปยังหน้า login ที่กำหนด ที่ /auth/ (หน้าเข้าสู่ระบบ)
    #PermissionRequiredMixin Mixin ที่ใช้กำหนดว่าผู้ใช้ต้องมีสิทธิ์ (permissions) เพื่อเข้าถึง View นี้ได้
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.delete_repairrequest"]# สิทธิ์ที่ ผู้เข้าถึงต้องมี 

    def get(self, request):#เป็นการเรียกดูข้อมูล
        try:
            userprofile = request.user.id #การเก็บ ID ของ Userที่ login
            student_target = Student.objects.get(user__id = request.user.id) #การ get นักศึกษาที่มี ID เดียวกันกับผู้ใช้
            request_status = RepairRequest.objects.filter(student__user__id= userprofile) #การ หาปัญหาที่นักศึกษาที่ login เป็นคนเขียน
            context = {"request_status": request_status, "student_target": student_target}
        #context เป็น ตัวแปลที่เป็นการสร้าง dictionary เพื่อส่งไปยังเทมเพลตสำหรับการแสดงหน้าเว็บ (student2.html)ผ่าน render() ของ Django

            return render(request, 'student2.html', context)
        except (Student.DoesNotExist or RepairRequest.DoesNotExist):
            return render(request, '500.html')

    def delete(self, request, request_id):
        print(request_id)

        i = RepairRequest.objects.get(pk = request_id)
        print(i)
        i.delete()

    #     return JsonResponse({'message': 'Employee added successfully'}, status=200)# status = 200 request ที่ client ขอมาได้รับการดำเนินการสำเร็จและไม่มีข้อผิดพลาด

#fam
class DeleteStatusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.delete_repairrequest"]

    def get(self, request, pk):
        #เมื่อมีคำขอ request delete ปัญหาที่ได้เขียนไปแต่ยังไม่มีการรับงานก็จะสามารถ ลบได้
        status = get_object_or_404(RepairRequest, pk=pk)#การ get ปัญหาตาม pk ที่ได้รับมาจาก pk ที่ส่งมาจาก path "deletestatus/<int:pk>/"
        status.delete()#นำปัญหาที่ get มาทำการลบ
        return redirect('trackstatus')#และทำการ ไปที่หน้า trackstatus ของนักศึกษา


# class StatusDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
#     login_url = '/auth/'
#     permission_required = ["SDMAS.view_repairrequest", "SDMAS.delete_repairrequest"]

#     def get(self, request, pk):
#         request1 = RepairRequest.objects.get(id = pk)
#         form = RepairRequestForm(instance=request1)
#         context = {"form": form}
#         return render(request, "editrequest.html", context)


class EditDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.change_repairrequest"]

    def get(self, request, pk):
        # การ get obj RepairRequest จาก pk ที่ได้มาจาก url ถ้าไม่ีจะขึ้น error 404
        request1 = get_object_or_404(RepairRequest, pk=pk)
        #การ get นักศึกษาที่มี ID เดียวกันกับผู้ใช้
        student_target = Student.objects.get(user__id = request.user.id)
        # ในตัวแปร form นี้มี RepairRequestForm เป็น form และมีการใช้ instance ซึ่งเป็นการนำข้อมูลที่ได้ get มาส่งลงใน form ที่ใส่ได้ที่ obj เลยเป็นเพราะว่า form ได้สร้างแบบ modelModelForm ที่ใช้ model RepairRequest
        form = RepairRequestForm(instance=request1)

        context = {"form": form, "student_target": student_target}
        return render(request, "editrequest.html", context)

    def post(self, request, pk):

        form = RepairRequestForm(request.POST)
        student_target = Student.objects.get(user__id = request.user.id)

        # เป็น function ที่ใช้ในการตรวจสอบว่าผู้ใช้ได้กรอกข้อมูลตาม กฎที่ได้กำหนดไว้ใน form หรือ ไม่
        if form.is_valid():
            request1 = get_object_or_404(RepairRequest, pk=pk)
            #การนำข้อมูลจาก ฟิว ที่ผู้ใช้กรอกในฟอร์มมาใช้งาน เป็น dictionary มาใส่ในตัวแปร
            description = form.cleaned_data["description"]
            urgency = form.cleaned_data["urgency"]
            timee = form.cleaned_data["repair_appointment_time"]
            #จากนั้นทำการ นำข้อมูลที่ได้มา update ตัว RepairRequest
            request1.description = description
            request1.urgency = urgency
            request1.repair_appointment_time = timee
            request1.save()
            return redirect("trackstatus")
        else:
            context = {"form": form, "student_target": student_target}
            return render(request, 'editrequest.html', context)

#fam
class StaffView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.delete_repairrequest"]


    def get(self, request):
        request_status = RepairRequest.objects.all()#การนำ ปัญหาของนักษาที่หมดมาเก็บไว้ที่ตัวแปร request_status
        context = {"request_status": request_status}

        return render(request, 'staff1.html', context)

    # def delete(self, request, request_id):
    #     i = RepairRequest.objects.get(pk = request_id)#การนำ ปัญหาของนักษาที่หมดมาเก็บไว้ที่ตัวแปร request_status
    #     i.delete()

    #     return JsonResponse({'message': 'Employee added successfully'}, status=200)

#fam
class StaffAssignDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.add_repairrequest", "SDMAS.add_repairassignment", "SDMAS.view_repairassignment"]

    def get(self, request, pk):
        # get_object_or_404()เป็น function ที่ดึงข้อมูล obj จากฐานข้อมูล หากไม่พบออบเจกต์ที่ตรงกับเงื่อนไขที่ระบุ มันจะส่งกลับ HTTP 404 (ไม่พบหน้า)
        request1 = get_object_or_404(RepairRequest, pk=pk)
        # ในตัวแปร form นี้มี StaffAssignmentForm เป็น form และมีการใช้ instance ซึ่งเป็นการนำข้อมูลที่ได้ get มาส่งลงใน form ที่ใส่ได้ที่ obj เลยเป็นเพราะว่า form ได้สร้างแบบ modelModelForm ที่ใช้ model RepairRequest
        form = StaffAssignmentForm(instance=request1)
        context = {"form": form, "repairrequest": request1}
        return render(request, "staff2.html", context)
    
    def post(self, request, pk):
        # post คือการรับค่าจาก user มาสร้าง REpairAssignment
        #ตัวแปร form ได้เก็บค่าที่ user ได้เขียนน form StaffAssignmentForm เข้ามา
        form = StaffAssignmentForm(request.POST)

        # เป็น function ที่ใช้ในการตรวจสอบว่าผู้ใช้ได้กรอกข้อมูลตาม กฎที่ได้กำหนดไว้ใน form หรือ ไม่
        if form.is_valid():
            request1 = get_object_or_404(RepairRequest, pk=pk)
            #คือการดึงข้อมูลจากฟิลด์ technician ที่ผู้ใช้กรอกในฟอร์มมาใช้งาน เป็น dictionary
            technician_assign = form.cleaned_data["technician"]
            for i in technician_assign:
                subject = 'Staff Had Assigned Appointment for '+str(i.user.first_name)+" "+str(i.user.last_name)
                message = 'โปรดทำการเช็คงานที่คุณได้รับมอบหมาย ในหน้ารับงานเพื่อดำเนินการต่อ'
                recipient_list = []
                recipient_list.append(str(i.user.email))

                # Send the email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )
            request1.status = "Assigned"
            request1.save()
            repair_assignment_create, created = RepairAssignment.objects.get_or_create(
                repair_request = request1, status = "Reported"
            )
            # repair_assignment_create ทำการ เพิ่ม technician ที่จำเป็นต้องใช้ " * " เพราะว่า technician_assign เป็น list เพราะใน technician เป็น many to many
            repair_assignment_create.technician.add(*technician_assign)
            repair_assignment_create.save()
            return redirect("staff")
        else:
            return render(request, "staff2.html", {"form":form})

#panda
class StaffManageStudentView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_student"]

    def get(self, request):
        # การ Query ข้อมูลของ student ใส่ในตัวแปร request_student 
        request_student = Student.objects.all()
        
        context = {"request_student": request_student}
        return render(request, "staff5.html", context)

#panda 
class StaffManageEditStudentView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.change_student", "SDMAS.view_student"]


    def get(self, request, pk):

        request_student = get_object_or_404(Student, pk=pk)
        form = StudentInfoForm(instance=request_student, pk = pk)
        context = {"request_student": request_student, "form": form}
        return render(request, "staff5edit.html", context)

    def post(self, request, pk):
        request_student = get_object_or_404(Student, pk=pk)

        # request.POST คือข้อมูลที่ user ได้กรอกไว้ ด้วยมี request_student เป็นข้อมูลที่ค้างอยู่ในแต่ละช่อง
        form = StudentInfoForm(request.POST, instance=request_student)

        # ตรวจสอบว่าค่าได้ที่ได้รับมาเป็นค่าที่ตรงตามกฎที่กำหนดรึป่าว
        if form.is_valid():
            form.save()
            return redirect("managestudent")
        else:
            return redirect("editstudent", pk=pk)

#panda การลบข้อมูล
class StaffManageDeleteStudentView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.delete_student", "SDMAS.view_student"]

    def get(self, request, pk):
        student_target = Student.objects.get(pk=pk)
        student_target.user.delete()
        student_target.delete()
        return redirect("managestudent")

#panda การแก้ไข requestassign ในเพิ่มช่างได้
class StaffAssignEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.change_repairrequest", "SDMAS.view_repairassignment", "SDMAS.change_repairassignment", "SDMAS.add_repairassignment"]

    def get(self, request, pk):
        request1 = get_object_or_404(RepairRequest, pk=pk)
        request2 = get_object_or_404(RepairAssignment, repair_request__id = pk)
        form = StaffAssignmentForm(instance=request1)
        context = {"form": form, "repairrequest": request1, "technician_list": request2}
        return render(request, "staff6.html", context)

    def post(self, request, pk):
        form = StaffAssignmentForm(request.POST)
        if form.is_valid():
            request1 = get_object_or_404(RepairRequest, pk=pk)
            request1.status = "Assigned"
            request1.save()
            technician_assign = form.cleaned_data["technician"]
            repair_assignment_create, created_check = RepairAssignment.objects.get_or_create(
                repair_request = request1
            )
            # panda อธิบาย
            if not created_check:
                alert = """<div class="alert alert-danger d-flex align-items-center" role="alert">
                                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                                <div>
                                    An example danger alert with an icon
                                </div>
                            </div>"""
                
            repair_assignment_create.technician.add(*technician_assign)
            repair_assignment_create.save()

            # ที่จำเป็นต้อง loop เพราะว่า technician_assign Queryset
            for i in technician_assign:
                subject = 'Staff Had Assigned Appointment for '+str(i.user.first_name)+" "+str(i.user.last_name)
                message = 'โปรดทำการเช็คงานที่คุณได้รับมอบหมาย ในหน้ารับงานเพื่อดำเนินการต่อ'
                recipient_list = []#สร้าง list เพิ่มเก็น email ที่ต้องการจะจะส่ง
                recipient_list.append(str(i.user.email))

                # Send the email
                send_mail(
                    subject,# หัวข้อ
                    message,# ข้อมความ
                    settings.DEFAULT_FROM_EMAIL,# email ที่เป็นคนส่ง
                    recipient_list,# emailที่เป็นคนรับ
                    fail_silently=False,# หากเกิดข้อผิดพลาดในขณะส่งอีเมล จะไม่ซ่อนข้อผิดพลาดนั้น (ทำให้การส่งล้มเหลวไม่ถูกเพิกเฉย)
                )
            return redirect("staffassignedit", pk=pk)
        else:
            request1 = get_object_or_404(RepairRequest, pk=pk)
            form = StaffAssignmentForm(instance=request1)
            return render(request, "staff6.html", {"form":form,"alert": alert})

#panda
class DeleteTechnicianAssignView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairassignment"
                           , "SDMAS.delete_repairassignment"
                           , "SDMAS.view_technician"]

    def get(self, request, pk, tech_id):
        repair_assign = RepairAssignment.objects.get(id=pk)
        technician_target = Technician.objects.get(pk = tech_id)
        # การที่ให้ repair_assign ลบ technician_target ออกจากความสัมพันธ์ m2m
        repair_assign.technician.remove(technician_target)
        subject = 'Staff Had Delete You ( '+str(technician_target.user.first_name)+" "+str(technician_target.user.last_name)+" ) From This Assignment"
        message = 'ทางเราต้องขออภัยในความไม่สะดวก แต่ทาง Staff ได้ตัดสินใจในการ ลบ คุณออกจาก Assignment นี้\nจึงเรียนมานะที่นี้, Staff'
        recipient_list = []
        recipient_list.append(str(technician_target.user.email))

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        return redirect("staffassignedit", pk=repair_assign.repair_request.id)

class StaffManageTechnicianView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_technician"
                           , "SDMAS.change_technician"
                           , "SDMAS.delete_technician"]

    def get(self, request):
        request_technician = Technician.objects.all()
        context = {"request_technician": request_technician}
        return render(request, "staff4.html", context)

#panda
class StaffManageEditTechnicianView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_technician"
                           , "SDMAS.change_technician"]

    def get(self, request, pk):
        request_technician = get_object_or_404(Technician, pk=pk)
        form = TechnicianInfoForm(instance=request_technician)
        context = {"request_technician": request_technician, "form": form}
        return render(request, "staff4edit.html", context)

    def post(self, request, pk):
        request_technician = get_object_or_404(Technician, pk=pk)

        form = TechnicianInfoForm(request.POST, instance=request_technician)
        if form.is_valid():
            form.save()
            return redirect("managetechnician")
        else:
            return redirect("edittechnician", pk=pk)

#panda
class StaffManageDeleteTechnicianView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_technician"
                           , "SDMAS.delete_technician"]

    def get(self, request, pk):
        technician_target = Technician.objects.get(pk=pk)
        technician_target.user.delete()
        technician_target.delete()
        return redirect("managetechnician")

#panda
class StaffHistoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairhistory"
                           , "SDMAS.view_room"
                        ]

    def get(self, request):
        history_target = RepairHistory.objects.all()
        room = Room.objects.all()
        context = {"history_target": history_target, "room": room}
        return render(request, 'history.html', context)
    
    def post(self, request):
        # ส่งข้อมูลโดนไม่ได้ผ่าน form จาก django
        target_room = request.POST.get('selectroom')
        if target_room == "empty":
            history_target = RepairHistory.objects.all()
            room = Room.objects.all()
            context = {"history_target": history_target, "room": room}
        else:
            history_target = RepairHistory.objects.all()
            room = Room.objects.all()
            history_list = RepairHistory.objects.filter(room__id = target_room)
            context = {"history_target": history_target, "history_list":history_list, "room": room}
        return render(request, 'history.html', context)

#panda
class StaffRoomView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairhistory"
                           , "SDMAS.view_room"
                        ]

    def get(self, request):
        room_list = Room.objects.all()
        context = {"room_list": room_list}
        return render(request, 'staffroom.html', context)

class StaffEditRoomView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairhistory"
                           , "SDMAS.view_room"
                        ]

    def get(self, request, pk):
        request_room = get_object_or_404(Room, pk=pk)

        form = RoomAddForm(instance=request_room)
        context = {"request_room": request_room, "form": form}
        return render(request, "staffroomedit.html", context)

    def post(self, request, pk):
        request_room = get_object_or_404(Room, pk=pk)

        form = RoomAddForm(request.POST, instance=request_room)
        if form.is_valid():
            form.save()
            return redirect("room")
        else:
            return redirect("editroom", pk=pk)

class StaffDeleteRoomView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairhistory"
                           , "SDMAS.view_room"
    ]

    def get(self, request, pk):
        i = Room.objects.get(pk = pk)
        i.delete()

        return redirect("room")

#panda
class RedirectView(View):
    def get(self, request):
        return redirect("login")

#fam
class TechnicianView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairassignment"]

    def get(self, request):
        try:
            userprofile = request.user.id
            technician_target = Technician.objects.get(user__id = userprofile)
            assignment_status = RepairAssignment.objects.filter(technician__user__id=userprofile)
            context = {"assignment_status": assignment_status, 'technician_target': technician_target}

            return render(request, 'Technician.html', context)
        except (Technician.DoesNotExist or RepairAssignment.DoesNotExist):
            return render(request, '500.html')
    
    def permission_denied(self, request, exception=None):
        return HttpResponseForbidden(render(request, '403.html'))

#fam
class TechnicianEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairstatusupdate"]

    def get(self, request):
        try:
            userprofile = request.user.id
            assignment_status = RepairStatusUpdate.objects.filter(technician__user__id=userprofile)
            technician_target = Technician.objects.get(user__id = userprofile)
            context = {"assignment_status": assignment_status, 'technician_target': technician_target}

            return render(request, 'TechnicianEdit.html', context)
        except (Technician.DoesNotExist or RepairStatusUpdate.DoesNotExist):
            return render(request, '500.html')

#fam
class TechnicainDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairassignment"
                           ,"SDMAS.change_repairassignment"
                           ,"SDMAS.add_repairstatusupdate"
                           ,"SDMAS.change_repairrequest"
                           ,"SDMAS.view_repairrequest"
                           ]

    def get(self, request, pk):
        technician_target = Technician.objects.get(user__id = request.user.id)
        requestassignment = get_object_or_404(RepairAssignment, pk=pk)
        request1 = get_object_or_404(RepairRequest, pk=requestassignment.repair_request.id)
        
        form = TechnicainAssignmentForm(instance=request1)
        context = {"form": form, "repairrequest": request1, "requestassignment": requestassignment, 'technician_target': technician_target}
        return render(request, "TechnicianDetail.html", context)
    
    def post(self, request, pk):
        try:
            userprofile = request.user.id
            technician = Technician.objects.get(user__id= userprofile)
            requestassignment = get_object_or_404(RepairAssignment, pk=pk)
            request1 = get_object_or_404(RepairRequest, pk=requestassignment.repair_request.id)
            requestassignment.status = "Assigned"
            requestassignment.save()
            repair_status_update_create = RepairStatusUpdate.objects.create(
                repair_request = request1, status = "Assigned"
            )
            # ต้องอัพเดต status
            repair_status_update_create.technician.add(technician)
            repair_status_update_create.save()
            subject = 'Notification Status Update for '+str(request1.student.user.first_name)+" "+str(request1.student.user.last_name)
            message = 'สถานะของคุณถูกอัพเดตเป็น '+str(requestassignment.status)
            recipient_list = []
            recipient_list.append(str(request1.student.user.email))

            # Send the email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            return redirect("technicianedit")
        except (Technician.DoesNotExist or RepairAssignment.DoesNotExist or RepairRequest.DoesNotExist):
            return render(request, '500.html')


#fam
class TechnicainUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairassignment"
                           ,"SDMAS.view_repairrequest"
                           ,"SDMAS.view_repairstatusupdate"
                           ,"SDMAS.add_repairstatusupdate"
                           ,"SDMAS.add_repairhistory"
                           ,"SDMAS.change_repairassignment"
                           ,"SDMAS.change_repairrequest"
                           ,"SDMAS.change_repairstatusupdate"
                           ]

    def get(self, request, pk):
        technician_target = Technician.objects.get(user__id = request.user.id)
        requestupdate = get_object_or_404(RepairStatusUpdate, pk=pk)
        request1 = get_object_or_404(RepairRequest, pk=requestupdate.repair_request.id)
        form = TechnicainUpdateForm(instance=request1)
        context = {"form": form, "repairrequest": request1, "requestupdate": requestupdate, 'technician_target': technician_target}
        return render(request, "TecUpdateStatus.html", context)
    
    def post(self, request, pk):
        form = TechnicainUpdateForm(request.POST)
        if form.is_valid():

            requestupdate = get_object_or_404(RepairStatusUpdate, pk=pk)

            request1 = get_object_or_404(RepairRequest, pk=requestupdate.repair_request.id)

            requestassignment = get_object_or_404(RepairAssignment, repair_request=request1)
            #การดึง ข้อมูลจาก ฟิว status จาก form
            status = form.cleaned_data["status"]
            # การสร้างเงื่อนไขว่า ถ้า status มีค่าเท่ากับ Completed หรือ completed จะตรงตามเงื่อนไข
            if status == "Completed" or status == "completed":
                #ทำการสร้าง RepairHistory และให้ repair_what fk ไปที่ requestupdate
                repair_history = RepairHistory.objects.create(
                    repair_what = requestupdate
                    )
                repair_history.room.add(request1.student.room_id)#ทำการเพิ่มห้อง
                repair_history.save()
            requestassignment.status = status
            requestassignment.save()
            request1.status = status
            request1.save()
            requestupdate.status = status
            requestupdate.save()

            subject = 'Notification Status Update for '+str(request1.student.user.first_name)+" "+str(request1.student.user.last_name)
            message = 'สถานะของคุณถูกอัพเดตเป็น '+str(requestassignment.status)
            recipient_list = []
            recipient_list.append(str(request1.student.user.email))

            # Send the email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            return redirect("technicianedit")
        else:
            requestupdate = get_object_or_404(RepairStatusUpdate, pk=pk)
            request1 = get_object_or_404(RepairRequest, pk=requestupdate.repair_request.id)
            form = TechnicainUpdateForm(instance=request1)
            context = {"form": form, "repairrequest": request1, "requestupdate": requestupdate}
            return render(request, "TecUpdateStatus.html", context)

#fam
class StudentTrackStatusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairstatusupdate"]

    def get(self, request):
        try:
            userprofile = request.user.id
            student_target = Student.objects.get(user__id = request.user.id)
            request_update = RepairStatusUpdate.objects.filter(repair_request__student__user__id= userprofile)
            context = {"request_update": request_update, "student_target": student_target}

            return render(request, 'student-trackstatus.html', context)
        except (Technician.DoesNotExist or RepairAssignment.DoesNotExist or RepairRequest.DoesNotExist):
            return render(request, '500.html')



class StaffAddRoomView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/'
    permission_required = ["SDMAS.view_repairrequest", "SDMAS.add_repairrequest"]

    def get(self, request):
        
        form = RoomAddForm()
        return render(request, 'roomadd.html', {"form":form})
    
    def post(self, request):
        
         # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = RoomAddForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                room_number = form.cleaned_data["room_number"]
                floor = form.cleaned_data["floor"]
                room_create = Room.objects.create(
                    room_number = room_number,
                    floor = floor
                )
                room_create.save()

                return redirect("room-add")
            else:
                return render(request, 'roomadd.html', {"form":form})

# class RepairRequestListView(APIView):
#     # def get(self, request):
#     #     students = RepairRequest.objects.all()
#     #     serializer = RepairRequestDjangotoNextJSSerializer(students, many=True)
#     #     return Response(serializer.data) #ส่งข้อมูลไปเป็น json
#     # permission_classes = [IsAuthenticated]  # ต้องล็อกอินก่อนใช้ API

#     def get(self, request):
#         try:
#             student = request.user.student  # ดึง student ของ user ที่ล็อกอิน
#             repair_requests = RepairRequest.objects.filter(student=student)  # ดึงเฉพาะของ student นี้
#             serializer = RepairRequestDjangotoNextJSSerializer(repair_requests, many=True)
#             return Response(serializer.data)
#         except Student.DoesNotExist:
#             return Response({"error": "Student not found"}, status=404)


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
    
#fam
class RepairUpdateListView(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     technician_id = request.query_params.get("technician_id", None)
        
    #     if not technician_id:
    #         return Response({"error": "Missing technician_id"}, status=400)
        
    #     try:
    #         technician = Technician.objects.get(id=technician_id, user=request.user)
    #         repair_statusupdate = RepairStatusUpdate.objects.filter(technician=technician)
    #         serializer = RequestUpdateDjangotoNextJSSerializer(repair_statusupdate, many=True)
    #         return Response(serializer.data)
    #     except Student.DoesNotExist:
    #         return Response({"error": "Student not found"}, status=404)
        
    # def delete(self, request, repair_request_id):
    #     """
    #     ลบ RepairRequest โดยต้องเป็นเจ้าของเท่านั้น
    #     """
    #     repair_request = get_object_or_404(RepairRequest, id=repair_request_id)

    #     # ตรวจสอบว่า repair_request เป็นของ student นี้หรือไม่
    #     if repair_request.student.user != request.user:
    #         return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    #     repair_request.delete()
    #     return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    def get(self, request, id):
        try:
            repair_update = RepairStatusUpdate.objects.get(id=id)
            serializer = RequestUpdateDjangotoNextJSSerializer(repair_update)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RepairRequest.DoesNotExist:
            return Response({"error": "Repair request not found"}, status=status.HTTP_404_NOT_FOUND)

#Staff - Index Page

class RepairRequestListViewStaff(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repair_requests = RepairRequest.objects.all()  # ดึงข้อมูลทั้งหมด
        serializer = RepairRequestDjangotoNextJSSerializer(repair_requests, many=True)
        return Response(serializer.data)

#Staff - AssignJob Filter By ID

class RepairRequestFilteredbyIDViewStaff(APIView):

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
        
    # def delete(self, request, repair_request_id):
    #     """
    #     ลบ RepairRequest โดยต้องเป็นเจ้าของเท่านั้น
    #     """
    #     repair_request = get_object_or_404(RepairRequest, id=repair_request_id)

    #     # ตรวจสอบว่า repair_request เป็นของ student นี้หรือไม่
    #     if repair_request.student.user != request.user:
    #         return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    #     repair_request.delete()
    #     return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class RepairRequestFilteredbyIDView(APIView):
    def get(self, request, id):
        try:
            repair_request = RepairRequest.objects.get(id=id)
            serializer = RepairRequestDjangotoNextJSSerializer(repair_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RepairRequest.DoesNotExist:
            return Response({"error": "Repair request not found"}, status=status.HTTP_404_NOT_FOUND)
        
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
