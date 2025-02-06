from django import forms
from .models import *
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError
from datetime import datetime, timezone
from django.db import transaction

from django.db import models
from django import forms

from SDMAS.models import *

class RepairRequestForm(ModelForm): # Form ของการกรอกข้อมุลแจ้งให้ซ่อม
    # SplitDateTimeField คือ function ที่แยก data and time ออกจากกัน
    repair_appointment_time = SplitDateTimeField(widget=SplitDateTimeWidget(
                date_attrs={"class": "input", "type": "date"},
                time_attrs={"class": "input", "type": "time"}
    )) #Input Field ที่มีช่องกรอกวันที่และเวลาแยกออกจากกัน

    class Meta:
        model = RepairRequest #นำโครงสร้างมาจาก Model RepairRequest
        fields = ['description',
            'urgency',
            'repair_appointment_time'
        ]


    def clean_repair_appointment_time(self): # กำหนด Function ขึ้นมาป้องกันการกรอกวันและเวลาที่เป็นอดีต
        repair_appointment_time = self.cleaned_data['repair_appointment_time'] # รับค่า repair_appointment_time ที่เป็น SplitDateTimeField มาเก็บในตัวแปร SplitDateTimeField

        if repair_appointment_time < datetime.now(timezone.utc): # เช็คว่าค่าที่กรอกว่ามีค่าน้อยกว่าวันและเวลาปัจจุบันหรือไม่
            raise ValidationError("The repair appointment time cannot be in the past.") # หากน้อยกว่าให้ขึ้น Error นี้

        return repair_appointment_time

class StaffAssignmentForm(ModelForm): # Form ในการ Assign งานให้ช่างซ่อมโดย Staff

    class Meta:
        model = RepairAssignment #นำโครงสร้างมาจาก Model RepairAssignment
        fields = [
            'technician'
        ]
        widgets = {
            "technician" : forms.SelectMultiple(attrs={
                "class" : "form-select"
            })
        } # การใช้ widgets ในการกำหนด input field ของ technician ให้สามารถเลือกได้หลายตัวเลือก

class TechnicainAssignmentForm(ModelForm): # Form ในการที่ช่างซ่อมจะกดรับงานที่ได้รับมอบหมายได้

    status = forms.ChoiceField(
        choices=[
            ('assigned', 'Assigned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        widget=forms.Select
    ) # Custom Field ที่กำหนดเป็น ChoiceField เพื่อให้เลือกสถานะได้

    class Meta:
        model = RepairAssignment #นำโครงสร้างมาจาก Model RepairAssignment
        fields = ['status']

class StudentInfoForm(ModelForm): # Form ที่จะจัดการเพิ่ม ลบ แก้ไขข้อมูลของนักศึกษาในหอพักโดย Staff

    full_name  = forms.CharField(max_length=255, required=True) # Custom Field ในการ input ชื่อ - นามสกุลด้วยกัน
    room_number = forms.ModelChoiceField(queryset=Room.objects.all()) # Custom Field ในการ input เลขห้องพัก

    class Meta:
        model = Student #นำโครงสร้างมาจาก Model Student
        fields = [
        ]
    
    def clean_full_name(self): # ฟังก์ชั่นในการแยกชื่อ - นามสกุลออกจากกัน
        full_name = self.cleaned_data['full_name'].strip() # การรับค่า full_name มา และตัด whitespace ทั้งหน้าและหลังออก
        name_parts = full_name.split() # แยก String ออกเป็น List

        if len(name_parts) < 2: # เช็คว่าใน Input Field มีสองส่วน (ชื่อ - นามสกุล) หรือไม่
            raise forms.ValidationError("Please enter both first name and surname.") # หากมีแค่ส่วนเดียวจะขึ้น Error นี้

        first_name = name_parts[0] # การนำค่าแรกของ List มาใส่เป็นชื่อ
        last_name = ' '.join(name_parts[1:]) #การนำค่าหลังจากอันแรกมาใส่เป็นนามสกุล (สามารถจัดการเรื่องมีชื่อกลางได้)
        return first_name, last_name

    def __init__(self, *args, **kwargs):
        room_id = kwargs.pop('pk', None) # การรับค่า room_id จาก kwargs ซึ่งเป็น keyword arguements เช่น { 'room_id' : 1 }
        super(StudentInfoForm, self).__init__(*args, **kwargs) # การเรียกใช้ Method '__init__' ของคลาสแม่หรือ ModelForm เพื่อกำหนดการส่งค่าทาง args และ kwargs

        if self.instance: # เช็คว่ามีข้อมูลของ Model Student อยู่แล้วหรือไม่ เพื่อแก้ไขโดยมิใช่การเพิ่มใหม่
            first_name = self.instance.user.first_name # การเก็บค่า first_name จากข้อมูลที่มีอยู่แล้วใน user.first_name
            last_name = self.instance.user.last_name # การเก็บค่า last_name จากข้อมูลที่มีอยู่แล้วใน user.last_name
            self.fields['full_name'].initial = f"{first_name} {last_name}" # การกำหนดค่าเริ่มต้นของ Field 'full_name' โดยนำ first_name และ last_name ด้านบนมาเชื่อมติดกันเป็น String เดียวกัน ส่วน initial คือการกำหนดค่าเริ่มต้น

        if room_id: # เช็คว่ามีข้อมูลของ room_id อยู่แล้วหรือไม่
            student = Student.objects.get(id=room_id) # ทำการ get object Model Student จากค่า room_id (ซึ่งเป็น id ของตัว student ห้องนั้นๆ)
            self.fields['room_number'].initial = student.room_id  # การกำหนดค่าเริ่มต้นของ Field 'room_number' จากข้อมูล student.room_id

    def save(self, commit=True): # การ override การ save ของ Form นี้
        student = super().save(commit=False) # การเรียกใช้เมธอด save จากคลาสแม่หรือ ModelForm แต่ยังไม่บันทึกลงไปในฐานข้อมูล (commit = False)
        if self.instance.user: # เช็คว่าทีข้อมูลของ user อยู่แล้วหรือไม่
            full_name = self.cleaned_data['full_name'] # รับค่าข้อมูลมาจาก Field 'full_name'

            student.user.first_name = full_name[0] # การบันทึกค่า user.first_name จาก index แรกของ full_name
            student.user.last_name = full_name[1] # การบันทึกค่า user.last_name จาก index ที่สองของ full_name
            student.room_id = self.cleaned_data['room_number'] # รับค่าข้อมูลมาจาก Field 'room_number' และนำมากำหนดใหเ student.room_id
            student.user.save() # บันทึกค่าของ user ใน Model Student
        if commit: # เช็คว่าสถานะ commit เป็น True หรือไม่
            student.save()  # หาก True จะ Save ข้อมูลลง Database
        return student

class TechnicianInfoForm(ModelForm): # Form ที่จะจัดการเพิ่ม ลบ แก้ไขข้อมูลของช่างโดย Staff

    full_name  = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Technician #นำโครงสร้างมาจาก Model Technician
        fields = [
            'expertise'
        ]

    def clean_full_name(self): # ฟังก์ชั่นในการแยกชื่อ - นามสกุลออกจากกัน
        full_name = self.cleaned_data['full_name'].strip() # การรับค่า full_name มา และตัด whitespace ทั้งหน้าและหลังออก
        name_parts = full_name.split() # แยก String ออกเป็น List

        if len(name_parts) < 2: # เช็คว่าใน Input Field มีสองส่วน (ชื่อ - นามสกุล) หรือไม่
            raise forms.ValidationError("Please enter both first name and surname.") # หากมีแค่ส่วนเดียวจะขึ้น Error นี้

        first_name = name_parts[0] # การนำค่าแรกของ List มาใส่เป็นชื่อ
        last_name = ' '.join(name_parts[1:]) #การนำค่าหลังจากอันแรกมาใส่เป็นนามสกุล (สามารถจัดการเรื่องมีชื่อกลางได้)
        return first_name, last_name

    def __init__(self, *args, **kwargs):

        super(TechnicianInfoForm, self).__init__(*args, **kwargs) # การเรียกใช้ Method '__init__' ของคลาสแม่หรือ ModelForm เพื่อกำหนดการส่งค่าทาง args และ kwargs

        if self.instance: # เช็คว่ามีข้อมูลของ Model Technician อยู่แล้วหรือไม่ เพื่อแก้ไขโดยมิใช่การเพิ่มใหม่
            first_name = self.instance.user.first_name # การเก็บค่า first_name จากข้อมูลที่มีอยู่แล้วใน user.first_name
            last_name = self.instance.user.last_name # การเก็บค่า last_name จากข้อมูลที่มีอยู่แล้วใน user.last_name
            self.fields['full_name'].initial = f"{first_name} {last_name}" # การกำหนดค่าเริ่มต้นของ Field 'full_name' โดยนำ first_name และ last_name ด้านบนมาเชื่อมติดกันเป็น String เดียวกัน

    def save(self, commit=True): # การ override การ save ของ Form นี้
        technician = super().save(commit=False) # การเรียกใช้เมธอด save จากคลาสแม่หรือ ModelForm แต่ยังไม่บันทึกลงไปในฐานข้อมูล (commit = False)
        if self.instance.user: # เช็คว่าทีข้อมูลของ user อยู่แล้วหรือไม่
            full_name = self.cleaned_data['full_name'] # รับค่าข้อมูลมาจาก Field 'full_name'
            technician.user.first_name = full_name[0] # การบันทึกค่า user.first_name จาก index แรกของ full_name
            technician.user.last_name = full_name[1] # การบันทึกค่า user.last_name จาก index ที่สองของ full_name
            technician.expertise = self.cleaned_data['expertise'] # รับค่าข้อมูลมาจาก Field 'expertise' และนำมากำหนดให้ technician.expertise
            technician.user.save() # บันทึกค่าของ user ใน Model Technician
        if commit: # เช็คว่าสถานะ commit เป็น True หรือไม่
            technician.save() # หาก True จะ Save ข้อมูลลง Database
        return technician

class TechnicainUpdateForm(ModelForm): # Form ที่จะทำให้ช่างสามารถ Update สถานะของงานตนเองได้

    status = forms.ChoiceField(
        choices=[
            ('assigned', 'Assigned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        widget=forms.Select
    )

    class Meta:
        model = RepairStatusUpdate #นำโครงสร้างมาจาก Model RepairStatusUpdate
        fields = ['status']
        widgets = {
            "technician" : forms.SelectMultiple(attrs={
                "class" : "form-select",
            })
        }

class RoomAddForm(ModelForm): # Form ที่จะทำให้เพิ่ม ลบ แก้ไข ห้องในหอพักได้โดยต้องเป็น Staff เท่านั้น

    class Meta:
        model = Room #นำโครงสร้างมาจาก Model Room
        fields = ['room_number', 'floor']
