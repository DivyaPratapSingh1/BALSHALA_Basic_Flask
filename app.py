from flask import Flask, render_template, request
from balshala.utils import bmi
from balshala.nutrition import calculate_tdee, calorie_target, macro_targets, generate_day_meal_plan
from balshala.scheduler import suggest_split
from balshala.plans import generate_workout_plan
from balshala.quotes import get_quote

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    age = int(request.form["age"])
    sex = request.form["sex"]
    height_cm = float(request.form["height"])
    weight_kg = float(request.form["weight"])
    activity = request.form["activity"]
    exp = request.form["experience"]
    goal = request.form["goal"]
    days = int(request.form["days"])
    pref = request.form["diet"]

    # Fake simple outputs (since core modules not available after reset)
    bmi_val = round(weight_kg / ((height_cm/100)**2), 1)
    tdee = 2000 + (weight_kg*5)  # simple placeholder
    target_cals = tdee * 0.9 if "Loss" in goal else (tdee*1.1 if "Gain" in goal else tdee)
    macros = {"protein_g": round(weight_kg*2,1), "carb_g": 200, "fat_g": 60}
    workout = {"name": "Full Body Split", "days": {"Day 1": ["Pushups", "Squats", "Rows"]}, "notes": "Basic progressive overload."}
    mealplan = {"meals": [{"meal": "Breakfast", "targets": macros, "suggestions": ["Oats", "Eggs", "Milk"]}]}
    quote = get_quote()

    return render_template("result.html",
                           age=age, sex=sex, height=height_cm, weight=weight_kg,
                           bmi_val=bmi_val, tdee=round(tdee,1), target_cals=round(target_cals,1),
                           macros=macros, workout=workout, mealplan=mealplan, quote=quote)

if __name__ == "__main__":
    app.run(debug=True)
