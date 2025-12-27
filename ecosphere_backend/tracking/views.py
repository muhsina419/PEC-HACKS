from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import EcoScan, EcoMiles, EcoWatt, EcoCycle
from .serializers import *

class EcoScanViewSet(viewsets.ModelViewSet):
    queryset = EcoScan.objects.all()
    serializer_class = EcoScanSerializer
    permission_classes = [permissions.IsAuthenticated]

class EcoMilesViewSet(viewsets.ModelViewSet):
    queryset = EcoMiles.objects.all()
    serializer_class = EcoMilesSerializer
    permission_classes = [permissions.IsAuthenticated]

class EcoWattViewSet(viewsets.ModelViewSet):
    queryset = EcoWatt.objects.all()
    serializer_class = EcoWattSerializer
    permission_classes = [permissions.IsAuthenticated]

class EcoCycleViewSet(viewsets.ModelViewSet):
    queryset = EcoCycle.objects.all()
    serializer_class = EcoCycleSerializer
    permission_classes = [permissions.IsAuthenticated]
