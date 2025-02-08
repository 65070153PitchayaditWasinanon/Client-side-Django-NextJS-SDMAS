from rest_framework import serializers
from .models import RepairRequest, RepairStatusUpdate
from .models import RepairRequest, Room, Student, RepairStatusUpdate
from django.contrib.auth.models import User
from rest_framework import serializers
from SDMAS.models import Room, Student


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username']

# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'user', 'room_id']