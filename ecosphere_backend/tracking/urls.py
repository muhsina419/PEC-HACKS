from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('ecoscan', EcoScanViewSet)
router.register('ecomiles', EcoMilesViewSet)
router.register('ecowatt', EcoWattViewSet)
router.register('ecocycle', EcoCycleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
