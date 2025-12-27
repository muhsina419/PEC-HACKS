import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FoodImpact, InventoryItem, UserAction
from .serializers import InventorySerializer
from .services import (
    ACTION_POINTS,
    calculate_eco_score,
    calculate_expiry,
    calculate_food_impact,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def scan_and_store(request):
    barcode = request.data.get("barcode")
    if not barcode:
        return Response({"error": "Barcode required"}, status=status.HTTP_400_BAD_REQUEST)

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    res = requests.get(url, timeout=10)

    if res.status_code != 200:
        return Response({"error": "Unable to fetch product"}, status=status.HTTP_502_BAD_GATEWAY)

    data = res.json()
    if data.get("status") != 1:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    product = data["product"]
    category = product.get("categories", "other")

    item = InventoryItem.objects.create(
        product_name=product.get("product_name"),
        brand=product.get("brands"),
        category=category,
        quantity=product.get("quantity"),
        packaging=product.get("packaging"),
        packaging_tags=product.get("packaging_materials_tags", []),
        eco_score=calculate_eco_score(product),
        image=product.get("image_front_url"),
        expiry_date=calculate_expiry(category),
    )

    return Response(InventorySerializer(item).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_inventory(request):
    items = InventoryItem.objects.all().order_by("expiry_date")
    return Response(InventorySerializer(items, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def log_user_action(request):
    item_id = request.data.get("item_id")
    action = request.data.get("action")

    if action not in ACTION_POINTS:
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = InventoryItem.objects.get(id=item_id)
    except InventoryItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    points = ACTION_POINTS[action]
    record = UserAction.objects.create(
        inventory_item=item,
        action=action,
        points_awarded=points,
    )

    return Response(
        {
            "message": "Action recorded",
            "points_awarded": record.points_awarded,
            "inventory_item": item.product_name,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def eco_food_scan(request):
    product = request.data.get("product")
    packaging = request.data.get("packaging", "")
    distance = float(request.data.get("distance", 0))

    if not product:
        return Response({"error": "Product name required"}, status=status.HTTP_400_BAD_REQUEST)

    carbon = calculate_food_impact(packaging, distance)

    FoodImpact.objects.create(
        user=request.user,
        product_name=product,
        packaging_type=packaging,
        distance_km=distance,
        carbon_kg=carbon,
        verified=True,
    )

    return Response(
        {
            "product": product,
            "carbon_kg": carbon,
            "packaging": packaging,
            "distance_km": distance,
        },
        status=status.HTTP_201_CREATED,
    )
