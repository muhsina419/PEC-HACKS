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

    return max(score, 0)


def calculate_food_impact(packaging, distance):
    score = 0

    if "plastic" in packaging:
        score += 2.5
    elif "paper" in packaging:
        score += 1

    score += distance * 0.3   # transport impact
    return round(score, 2)
