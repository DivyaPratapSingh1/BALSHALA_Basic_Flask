from typing import Dict, List

EXERCISES = {
    "push": [
        "Barbell Bench Press 3x6-8 (RPE 7-8)",
        "Overhead Press 3x6-10 (RPE 7-8)",
        "Incline DB Press 3x8-10",
        "Lateral Raises 3x12-15",
        "Triceps Pushdowns 3x10-12"
    ],
    "pull": [
        "Deadlift 3x3-5 (RPE 7-8)",
        "Pull-ups or Lat Pulldown 3x6-10",
        "Barbell Row 3x6-10",
        "Face Pulls 3x12-15",
        "Biceps Curls 3x10-12"
    ],
    "legs": [
        "Back Squat 3x5-8 (RPE 7-8)",
        "Romanian Deadlift 3x6-10",
        "Leg Press 3x10-12",
        "Leg Curls 3x10-12",
        "Calf Raises 3x12-15"
    ],
    "upper": [
        "Bench Press 3x6-8 (RPE 7-8)",
        "Barbell Row 3x6-10",
        "Overhead Press 3x6-10",
        "Lat Pulldown 3x8-12",
        "Face Pulls 3x12-15",
        "Curls 3x10-12",
        "Triceps Extensions 3x10-12"
    ],
    "lower": [
        "Back Squat 3x5-8 (RPE 7-8)",
        "Romanian Deadlift 3x6-10",
        "Leg Press 3x10-12",
        "Leg Curls 3x10-12",
        "Calf Raises 3x12-15",
        "Abs/Core 3x12-15"
    ],
    "full_body": [
        "Back Squat 3x5-8 (RPE 7-8)",
        "Bench Press 3x6-8",
        "Barbell Row 3x6-10",
        "Overhead Press 3x6-10",
        "Lat Pulldown or Pull-ups 3x8-12",
        "Curls or Triceps 3x10-12"
    ]
}

def progressive_overload_note():
    return ("Progressive Overload: If you hit the top of the rep range on all sets with good form, "
            "increase the load next session by ~2.5–5%. Keep 1–3 reps in reserve (RIR).")

def build_day(day_name: str) -> List[str]:
    dn = day_name.lower()
    if "push" in dn:
        return EXERCISES["push"]
    if "pull" in dn:
        return EXERCISES["pull"]
    if "leg" in dn:
        return EXERCISES["legs"]
    if "upper" in dn:
        return EXERCISES["upper"]
    if "lower" in dn:
        return EXERCISES["lower"]
    return EXERCISES["full_body"]

def generate_workout_plan(split: Dict) -> Dict:
    days = split["days"]
    plan = {}
    for d in days:
        plan[d] = build_day(d)
    return {
        "name": split["name"],
        "days": plan,
        "notes": progressive_overload_note()
    }
