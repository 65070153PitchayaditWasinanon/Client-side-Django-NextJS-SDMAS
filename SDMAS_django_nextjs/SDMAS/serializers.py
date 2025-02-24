from rest_framework import serializers
from .models import RepairRequest, RepairStatusUpdate
from .models import RepairRequest, Room, Student, RepairStatusUpdate, RepairAssignment,Technician
from django.contrib.auth.models import User
from rest_framework import serializers

#สำหรับ format ของ RepairRequest
class RepairRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = '__all__'  # หรือเลือกเฉพาะฟิลด์ที่ต้องการ เช่น ['description', 'urgency', 'repair_appointment_time']

#สำหรับ format ของ RepairStatusUpdate
class TechnicianRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairStatusUpdate
        fields = '__all__'  # หรือเลือกเฉพาะฟิลด์ที่ต้องการ เช่น ['description', 'urgency', 'repair_appointment_time']

#สำหรับ format ของ Room
class RoomDjangotoNextJSSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

#สำหรับ format ของ Student
class StudentDjangotoNextJSSerializer(serializers.ModelSerializer):
    room_id = RoomDjangotoNextJSSerializer() # เอาข้อมูลของตาราง Room มาใส่ในข้อมูลของ room_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = Student
        fields = '__all__'


#สำหรับ format ของ RepairRequest
class RepairRequestDjangotoNextJSSerializer(serializers.ModelSerializer):
    
    student = StudentDjangotoNextJSSerializer() # เอาข้อมูลของตาราง Student มาใส่ในข้อมูลของ student_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = RepairRequest
        fields = '__all__'

# Fam
class RepairRequest2DjangotoNextJSSerializer(serializers.ModelSerializer):
    
    student = StudentDjangotoNextJSSerializer() # เอาข้อมูลของตาราง Student มาใส่ในข้อมูลของ student_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = RepairRequest
        fields = '__all__'

# fam
class RepairAssignmentDjangotoNextJSSerializer(serializers.ModelSerializer):
    repair_request = RepairRequest2DjangotoNextJSSerializer() # เอาข้อมูลของตาราง Student มาใส่ในข้อมูลของ student_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = RepairAssignment
        fields = '__all__'

class RepairAssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairAssignment
        fields = "__all__"

# fam
class RequestUpdateDjangotoNextJSSerializer(serializers.ModelSerializer):
    repair_request = RepairRequestDjangotoNextJSSerializer() # เอาข้อมูลของตาราง Student มาใส่ในข้อมูลของ student_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = RepairStatusUpdate
        fields = '__all__'

class UserDJangotoNextJSSerializrs(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TechnicianDjangotoNextJSSerializer(serializers.ModelSerializer):
    user = UserDJangotoNextJSSerializrs()
    class Meta:
        model = Technician
        fields = '__all__'



class RepairAssignmentDjangotoNextJSSerailizer(serializers.ModelSerializer):
    repair_request = RepairRequestDjangotoNextJSSerializer()
    class Meta:
        model = RepairAssignment
        fields = '__all__'

#fam
class RoomDjangotoNextJSSerializer(serializers.ModelSerializer):
    # student = StudentDjangotoNextJSSerializer() # เอาข้อมูลของตาราง Student มาใส่ในข้อมูลของ student_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = Room
        fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username']

# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'user', 'room_id']
