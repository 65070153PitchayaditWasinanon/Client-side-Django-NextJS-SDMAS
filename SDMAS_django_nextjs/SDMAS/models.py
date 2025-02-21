from django.db import models

# Create your models here.
from django.db import models
from django.db.models import *

# Create your models here.

from django.contrib.auth.models import User

#เพิ่มตัวระบุ โดยการเลือกห้อง

class Room(models.Model):
    room_number = models.CharField(max_length=100, unique=True)
    floor = models.CharField(max_length=100)
    def __str__(self):
        return self.room_number

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    technician_id = models.CharField(max_length=20, unique=True)
    expertise = models.CharField(max_length=100) #อาจจะปรับเปลี่ยน

    def __str__(self): 
        return (self.user.first_name+" "+self.user.last_name)

# คำขอจากนศ
class RepairRequest(models.Model): 
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField() 
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    repair_appointment_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self): 
        return f"RepairRequest {self.id} by {self.student.user.username}"

# มอบหมายงานให้ technician
class RepairAssignment(models.Model):
    repair_request = models.OneToOneField(RepairRequest, on_delete=models.CASCADE)
    technician = models.ManyToManyField(Technician)
    assigned_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=20, choices=RepairRequest.STATUS_CHOICES, default='assigned')

# เมื่อรับงานแล้วจะสร้างตัวนี้
class RepairStatusUpdate(models.Model):
    repair_request = models.ForeignKey(RepairRequest, on_delete=models.CASCADE)
    technician = models.ManyToManyField(Technician)
    status = models.CharField(max_length=20, choices=RepairRequest.STATUS_CHOICES)
    update_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    read = models.BooleanField(default=False)

class RepairHistory(models.Model):
    repair_what = models.ForeignKey(RepairStatusUpdate, on_delete=models.CASCADE)
    room = models.ManyToManyField(Room)