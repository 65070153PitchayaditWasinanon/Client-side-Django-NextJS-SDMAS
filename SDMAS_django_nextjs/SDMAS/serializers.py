from rest_framework import serializers
from .models import RepairRequest

class RepairRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = '__all__'  # หรือเลือกเฉพาะฟิลด์ที่ต้องการ เช่น ['description', 'urgency', 'repair_appointment_time']