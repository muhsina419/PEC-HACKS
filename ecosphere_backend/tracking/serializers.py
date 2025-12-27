from rest_framework import serializers
from .models import EcoScan, EcoMiles, EcoWatt, EcoCycle

class EcoScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoScan
        fields = "__all__"

class EcoMilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoMiles
        fields = "__all__"

class EcoWattSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoWatt
        fields = "__all__"

class EcoCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoCycle
        fields = "__all__"
