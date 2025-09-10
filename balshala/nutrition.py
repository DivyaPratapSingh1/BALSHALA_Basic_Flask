import json, math, os
from pathlib import Path
from typing import Dict, Tuple
from .utils import mifflin_st_jeor_bmr, clamp

ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}

def calculate_tdee(sex: str, age: int, weight_kg: float, height_cm: float, activity_level: str) -> float:
    bmr = mifflin_st_jeor_bmr(sex, weight_kg, height_cm, age)
    factor = ACTIVITY_FACTORS.get(activity_level, 1.2)
    return bmr * factor

def calorie_target(tdee: float, goal: str) -> float:
    goal = goal.lower()
    if "fat" in goal or "loss" in goal or "cut" in goal:
        return tdee * 0.8  # ~20% deficit
    if "gain" in goal or "bulk" in goal or "muscle" in goal:
        return tdee * 1.15  # ~15% surplus
    return tdee  # maintenance

def macro_targets(weight_kg: float, calories: float, goal: str) -> Dict[str, float]:
    goal = goal.lower()
    # protein per kg
    if "fat" in goal or "loss" in goal:
        g_per_kg = 1.8
    elif "gain" in goal or "bulk" in goal or "muscle" in goal:
        g_per_kg = 2.0
    else:
        g_per_kg = 1.6
    protein_g = g_per_kg * weight_kg
    # fat: 25% calories
    fat_kcal = 0.25 * calories
    fat_g = fat_kcal / 9.0
    # carbs: rest
    remaining_kcal = calories - (protein_g * 4.0 + fat_g * 9.0)
    carb_g = max(0.0, remaining_kcal / 4.0)
    return {"protein_g": round(protein_g,1), "fat_g": round(fat_g,1), "carb_g": round(carb_g,1)}

def load_food_db() -> Dict:
    path = Path(__file__).resolve().parent.parent / "data" / "food_db.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"veg": {"protein":[], "carb":[], "fat":[]}, "nonveg": {"protein":[], "carb":[], "fat":[]}}

def generate_day_meal_plan(macros: Dict[str, float], pref: str="veg") -> Dict:
    """
    Very simple heuristic: break into 4 meals.
    Distribute protein ~30/30/20/20, carbs ~30/40/30, fat ~25/35/40 across meals.
    Then pick 2-3 items from DB for each meal.
    """
    food_db = load_food_db()
    key = "veg" if pref.lower().startswith("veg") else "nonveg"
    pro = macros["protein_g"]; carb = macros["carb_g"]; fat = macros["fat_g"]

    meal_shares = [
        {"name":"Breakfast", "p":0.3, "c":0.3, "f":0.25},
        {"name":"Lunch",     "p":0.3, "c":0.4, "f":0.35},
        {"name":"Snack",     "p":0.2, "c":0.15,"f":0.15},
        {"name":"Dinner",    "p":0.2, "c":0.15,"f":0.25},
    ]

    meals = []
    for m in meal_shares:
        target = {
            "protein_g": round(pro*m["p"],1),
            "carb_g": round(carb*m["c"],1),
            "fat_g": round(fat*m["f"],1),
        }
        # naive picks
        picks = []
        # pick one protein
        if food_db[key]["protein"]:
            picks.append(food_db[key]["protein"][hash(m["name"]) % len(food_db[key]["protein"])]["name"])
        # pick one carb
        if food_db[key]["carb"]:
            picks.append(food_db[key]["carb"][hash(m["name"]+"c") % len(food_db[key]["carb"])]["name"])
        # pick one fat
        if food_db[key]["fat"]:
            picks.append(food_db[key]["fat"][hash(m["name"]+"f") % len(food_db[key]["fat"])]["name"])
        meals.append({"meal": m["name"], "targets": target, "suggestions": picks})
    return {
        "macros_total": macros,
        "meals": meals
    }
