# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import InventoryItem
# from .serializers import InventorySerializer
# from datetime import date, timedelta
# import requests
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import InventoryItem, UserAction
# from .services import calculate_expiry, calculate_eco_score
# import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import InventoryItem
from .utils import calculate_expiry, calculate_eco_score
import requests

SHELF_LIFE = {
    "vegetables": 5,
    "dairy": 7,
    "bakery": 3,
    "meat": 3,
    "beverages": 180,
    "default": 7
}

def get_expiry(category):
    for key in SHELF_LIFE:
        if key in category.lower():
            return date.today() + timedelta(days=SHELF_LIFE[key])
    return date.today() + timedelta(days=7)


@api_view(["POST"])
def scan_and_store(request):
    barcode = request.data.get("barcode")
    if not barcode:
        return Response({"error": "Barcode required"}, status=400)

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    data = requests.get(url).json()

    if data.get("status") != 1:
        return Response({"error": "Product not found"}, status=404)

    product = data["product"]
    category = product.get("categories", "other")

    item = InventoryItem.objects.create(
        product_name=product.get("product_name"),
        brand=product.get("brands"),
        category=category,
        quantity=product.get("quantity"),
        packaging=product.get("packaging"),
        eco_score=calculate_eco_score(product),
        image=product.get("image_front_url"),
        expiry_date=get_expiry(category),
    )

    return Response(InventorySerializer(item).data)
@api_view(["GET"])
def get_inventory(request):
    items = InventoryItem.objects.all().order_by("expiry_date")
    serializer = InventorySerializer(items, many=True)
    return Response(serializer.data)
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import InventoryItem
from .utils import calculate_expiry, calculate_eco_score

@api_view(["POST"])
def scan_and_store(request):
    barcode = request.data.get("barcode")
    if not barcode:
        return Response({"error": "Barcode required"}, status=400)

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    res = requests.get(url)
    data = res.json()

    if data.get("status") != 1:
        return Response({"error": "Product not found"}, status=404)

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

    return Response({
        "id": item.id,
        "product_name": item.product_name,
        "eco_score": item.eco_score,
        "expiry_date": item.expiry_date
    })


@api_view(["GET"])
def list_inventory(request):
    items = InventoryItem.objects.all().order_by("expiry_date")
    data = [
        {
            "id": i.id,
            "name": i.product_name,
            "category": i.category,
            "eco_score": i.eco_score,
            "expiry": i.expiry_date,
            "days_left": i.days_left()
        }
        for i in items
    ]
    return Response(data)
from .models import UserAction
from .utils import ACTION_POINTS

@api_view(["POST"])
def log_user_action(request):
    item_id = request.data.get("item_id")
    action = request.data.get("action")

    if action not in ACTION_POINTS:
        return Response({"error": "Invalid action"}, status=400)

    try:
        item = InventoryItem.objects.get(id=item_id)
    except InventoryItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    points = ACTION_POINTS[action]

    record = UserAction.objects.create(
        inventory_item=item,
        action=action,
        points_awarded=points
    )

    return Response({
        "message": "Action recorded",
        "points": points,
        "total_impact": f"{points} points added"
    })
@api_view(["POST"])
def eco_food_scan(request):
    data = request.data

    product = data.get("product")
    packaging = data.get("packaging")
    distance = float(data.get("distance", 0))

    carbon = calculate_food_impact(packaging, distance)

    record = FoodImpact.objects.create(
        user=request.user,
        product_name=product,
        packaging_type=packaging,
        distance_km=distance,
        carbon_kg=carbon,
        verified=True
    )

    return Response({
        "product": product,
        "carbon_kg": carbon,
        "message": "Food impact recorded"
    })
