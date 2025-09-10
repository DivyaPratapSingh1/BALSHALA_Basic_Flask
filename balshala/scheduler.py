from typing import Dict

def suggest_split(days_per_week: int, experience: str) -> Dict:
    """
    Returns a dict describing the recommended split.
    """
    experience = (experience or "beginner").lower()
    d = days_per_week
    if d <= 3:
        return {"name": "Full Body (3-day) or PPL (3-day)",
                "days": ["Full Body A", "Full Body B", "Full Body C"]}
    if d == 4:
        return {"name": "Upper/Lower x2 (4-day)",
                "days": ["Upper A", "Lower A", "Upper B", "Lower B"]}
    if d == 5:
        return {"name": "UL + PPL Hybrid (5-day)",
                "days": ["Upper", "Lower", "Push", "Pull", "Legs"]}
    if d >= 6:
        return {"name": "Push/Pull/Legs x2 (6-day)",
                "days": ["Push A", "Pull A", "Legs A", "Push B", "Pull B", "Legs B"]}
    return {"name": "Flexible", "days": ["Day 1","Day 2","Day 3"]}
