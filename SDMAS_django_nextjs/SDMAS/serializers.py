from rest_framework import serializers
from .models import RepairRequest

class RepairRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
<<<<<<< HEAD
        fields = '__all__'  # หรือเลือกเฉพาะฟิลด์ที่ต้องการ เช่น ['description', 'urgency', 'repair_appointment_time']

class RepairRequestDjangotoNextJSSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = '__all__'
=======
        fields = '__all__'  # หรือเลือกเฉพาะฟิลด์ที่ต้องการ เช่น ['description', 'urgency', 'repair_appointment_time']
>>>>>>> 551337cd61209477b09c347cb1d4e6151aea2d9e
