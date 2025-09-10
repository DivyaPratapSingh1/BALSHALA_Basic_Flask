from typing import Literal

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def mifflin_st_jeor_bmr(sex: Literal["male","female"], weight_kg: float, height_cm: float, age: int) -> float:
    """
    Mifflin-St Jeor Equation:
    Male:   BMR = 10*W + 6.25*H - 5*A + 5
    Female: BMR = 10*W + 6.25*H - 5*A - 161
    """
    if sex == "male":
        return 10*weight_kg + 6.25*height_cm - 5*age + 5
    else:
        return 10*weight_kg + 6.25*height_cm - 5*age - 161

def bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100.0
    if h_m <= 0:
        return 0.0
    return weight_kg / (h_m * h_m)
