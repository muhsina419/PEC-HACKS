from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ElectricityBillSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_electricity_bill(request):
    serializer = ElectricityBillSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        bill = serializer.save()
        return Response(ElectricityBillSerializer(bill).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
