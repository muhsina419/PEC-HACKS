# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from datetime import date, timedelta
# import requests

# from .models import InventoryItem, UserAction
# from .utils import calculate_expiry, calculate_eco_score, ACTION_POINTS
# # from .serializers import InventorySerializer

# @api_view(["POST"])
# def scan_and_store(request):
#     barcode = request.data.get("barcode")

#     if not barcode:
#         return Response({"error": "Barcode required"}, status=400)

#     # Fetch from OpenFoodFacts
#     url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
#     response = requests.get(url)
#     data = response.json()

#     if data.get("status") != 1:
#         return Response({"error": "Product not found"}, status=404)

#     product = data["product"]
#     category = product.get("categories", "other")

#     item = InventoryItem.objects.create(
#         product_name=product.get("product_name"),
#         brand=product.get("brands"),
#         category=category,
#         quantity=product.get("quantity"),
#         packaging=product.get("packaging"),
#         packaging_tags=product.get("packaging_materials_tags", []),
#         eco_score=calculate_eco_score(product),
#         image=product.get("image_front_url"),
#         expiry_date=calculate_expiry(category),
#     )

#     return Response({
#         "id": item.id,
#         "product_name": item.product_name,
#         "eco_score": item.eco_score,
#         "expiry_date": item.expiry_date,
#     })
# @api_view(["GET"])
# def get_inventory(request):
#     items = InventoryItem.objects.all().order_by("expiry_date")
#     serializer = InventorySerializer(items, many=True)
#     return Response(serializer.data)
# @api_view(["POST"])
# def log_user_action(request):
#     item_id = request.data.get("item_id")
#     action = request.data.get("action")

#     if action not in ACTION_POINTS:
#         return Response({"error": "Invalid action"}, status=400)

#     try:
#         item = InventoryItem.objects.get(id=item_id)
#     except InventoryItem.DoesNotExist:
#         return Response({"error": "Item not found"}, status=404)

#     points = ACTION_POINTS[action]

#     UserAction.objects.create(
#         inventory_item=item,
#         action=action,
#         points_awarded=points
#     )

#     return Response({
#         "message": "Action recorded",
#         "points": points
#     })
from datetime import date, timedelta

SHELF_LIFE = {
    "vegetables": 5,
    "fruits": 7,
    "dairy": 7,
    "meat": 3,
    "bakery": 3,
    "beverages": 180,
    "default": 7,
}

ACTION_POINTS = {
    "recycled": 10,
    "reused": 15,
    "donated": 20,
    "discarded": -10,
}


def calculate_expiry(category):
    category = category.lower()
    for key in SHELF_LIFE:
        if key in category:
            return date.today() + timedelta(days=SHELF_LIFE[key])
    return date.today() + timedelta(days=SHELF_LIFE["default"])


def calculate_eco_score(product):
    score = 100
    packaging = product.get("packaging", "").lower()

    if "plastic" in packaging:
        score -= 25
    if "glass" in packaging:
        score -= 10
    if "paper" in packaging:
        score -= 5

    return score
