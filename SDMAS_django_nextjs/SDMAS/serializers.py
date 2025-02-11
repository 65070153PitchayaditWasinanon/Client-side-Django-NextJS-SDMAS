from rest_framework import serializers
from .models import RepairRequest, RepairStatusUpdate
from .models import RepairRequest, Room, Student, RepairStatusUpdate, RepairAssignment
from django.contrib.auth.models import User
from rest_framework import serializers

class RepairRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = '__all__'  # หรือเลือกเฉพาะฟิลด์ที่ต้องการ เช่น ['description', 'urgency', 'repair_appointment_time']

class TechnicianRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairStatusUpdate
        fields = '__all__'  # หรือเลือกเฉพาะฟิลด์ที่ต้องการ เช่น ['description', 'urgency', 'repair_appointment_time']

class RoomDjangotoNextJSSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

class StudentDjangotoNextJSSerializer(serializers.ModelSerializer):
    room_id = RoomDjangotoNextJSSerializer() # เอาข้อมูลของตาราง Room มาใส่ในข้อมูลของ room_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = Student
        fields = '__all__'

class RepairRequestDjangotoNextJSSerializer(serializers.ModelSerializer):
    student = StudentDjangotoNextJSSerializer() # เอาข้อมูลของตาราง Student มาใส่ในข้อมูลของ student_id เพราะถ้าส่ง API ไปจะเป็น json ทำให้ใช้การอ้างอิงโดยความสัมพันธ์ไม่ได้
    class Meta:
        model = RepairRequest
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
