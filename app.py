import streamlit as st
from datetime import date, datetime
import random
import pandas as pd

QUOTES = [
    "Small consistent steps beat sporadic heroics.",
    "Comfort is the enemy of progress.",
    "Train hard, recover harder.",
    "Progress is imperfect — keep showing up.",
    "Discipline is doing what's necessary, even when you don't feel like it."
]

DEFAULT = {"name":"", "age":18, "gender":"male", "weight":60, "goal":"muscle", "diet":"non-veg", "gym_days":3, "experience":"beginner"}

def ensure_state():
    if "profiles" not in st.session_state:
        st.session_state["profiles"] = {}
    if "logs" not in st.session_state:
        st.session_state["logs"] = {}

def estimate_calories(weight, goal):
    base = weight * 24
    if goal == "muscle": return int(base * 1.2)
    if goal == "fatloss": return int(base * 0.85)
    return int(base)

def suggest_split(gym_days):
    if gym_days <= 2: return "Full body - 2x per week"
    if gym_days == 3: return "Full body - 3x per week"
    if gym_days == 4: return "Upper / Lower split (4 days)"
    if gym_days == 5: return "Push / Pull / Legs + 2 accessory days (5 days)"
    return "Custom split — mix strength & conditioning"

def build_workout(goal, gym_days, experience):
    sessions = []
    if gym_days <= 3:
        for i in range(gym_days):
            sessions.append({
                "day": f"Day {i+1}",
                "focus": "Full body",
                "exercises":[
                    {"name":"Squat / Variation", "sets":3, "reps":"6-10"},
                    {"name":"Horizontal Push (Bench/Pushup)", "sets":3, "reps":"6-10"},
                    {"name":"Row", "sets":3, "reps":"6-10"},
                    {"name":"Accessory & Core", "sets":2, "reps":"10-15"}
                ]
            })
    else:
        for i in range(gym_days):
            if i % 3 == 0:
                focus = "Push (Chest/Shoulders/Triceps)"
                exercises = [
                    {"name":"Bench / Incline", "sets":4, "reps":"6-10"},
                    {"name":"Overhead Press", "sets":3, "reps":"6-10"},
                    {"name":"Triceps Accessory", "sets":3, "reps":"8-12"}
                ]
            elif i % 3 == 1:
                focus = "Pull (Back/Biceps)"
                exercises = [
                    {"name":"Deadlift / Hinge", "sets":3, "reps":"4-8"},
                    {"name":"Pull-up / Lat Pull", "sets":4, "reps":"6-10"},
                    {"name":"Biceps Accessory", "sets":3, "reps":"8-12"}
                ]
            else:
                focus = "Legs (Quads/Hamstrings)"
                exercises = [
                    {"name":"Squat / Variation", "sets":4, "reps":"6-10"},
                    {"name":"Romanian Deadlift", "sets":3, "reps":"6-10"},
                    {"name":"Leg Accessory", "sets":3, "reps":"8-12"}
                ]
            sessions.append({"day":f"Day {i+1}", "focus":focus, "exercises":exercises})
    for s in sessions:
        s["progression_tip"] = ("Increase load weekly by 2.5-5% if you complete upper rep range with good technique."
                                if experience != "beginner" else "Focus on technique for 4-6 weeks before adding heavy progression.")
    return sessions

def build_meal_plan(diet, calories):
    protein_target = int(calories * 0.25 / 4)
    meals = [
        {"time":"Breakfast", "items":["Oats / Upma / Poha", "2 Eggs or Soya/Paneer (if veg)", "Fruit"]},
        {"time":"Mid-Morning", "items":["Yogurt / Buttermilk", "Nuts (almonds/walnuts)"]},
        {"time":"Lunch", "items":["Roti / Rice", "Lentils or Chicken/Fish", "Vegetables/Salad"]},
        {"time":"Evening", "items":["Tea + Besan Chilla / Sprouts Salad", "Fruit"]},
        {"time":"Dinner", "items":["Roti / Quinoa", "Paneer or Fish/Chicken", "Salad"]}
    ]
    return {"calories":calories, "protein_goal_g":protein_target, "meals":meals}

ensure_state()
st.set_page_config(page_title="BALSHALA — AI Gym Coach", layout="wide")

st.sidebar.title("BALSHALA")
page = st.sidebar.radio("Navigate", ["Home", "Create Profile", "Generate Plan", "Progress Log", "About"])

if page == "Home":
    st.title("BALSHALA — AI Gym Coach")
    st.markdown("A demo Streamlit app that generates personalized workout and meal plans based on simple rule-templates. Session-only storage (no files).")
    st.markdown("---")
    col1, col2 = st.columns([3,1])
    with col1:
        st.header("Quick demo")
        st.write("Create a profile and generate a plan. Data lives in the active session and resets when the session ends or page refreshes.")
    with col2:
        st.info(random.choice(QUOTES))

elif page == "Create Profile":
    st.header("Create or Edit Profile")
    with st.form("profile_form"):
        name = st.text_input("Name", value=DEFAULT["name"])
        age = st.number_input("Age", value=DEFAULT["age"], min_value=10, max_value=80)
        gender = st.selectbox("Gender", options=["male","female","other"], index=0)
        weight = st.number_input("Weight (kg)", value=DEFAULT["weight"], min_value=20, max_value=200)
        goal = st.selectbox("Primary Goal", options=["muscle","fatloss","maintain"], index=0, format_func=lambda x: {"muscle":"Build Muscle","fatloss":"Fat Loss","maintain":"Maintenance"}[x])
        diet = st.selectbox("Dietary Preference", options=["non-veg","veg"], index=0, format_func=lambda x: {"non-veg":"Non-vegetarian","veg":"Vegetarian"}[x])
        gym_days = st.number_input("Gym days per week", value=DEFAULT["gym_days"], min_value=1, max_value=7)
        experience = st.selectbox("Experience level", options=["beginner","intermediate","advanced"], index=0)
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            profile = {"name":name, "age":age, "gender":gender, "weight":weight, "goal":goal, "diet":diet, "gym_days":int(gym_days), "experience":experience}
            st.session_state["profiles"][name] = profile
            if name not in st.session_state["logs"]:
                st.session_state["logs"][name] = []
            st.success("Profile saved in session.")

elif page == "Generate Plan":
    st.header("Generate Personalized Plan")
    profiles = list(st.session_state["profiles"].keys())
    if not profiles:
        st.warning("No profiles in session. Create one first.")
    else:
        selected = st.selectbox("Choose profile", profiles)
        profile = st.session_state["profiles"][selected]
        st.subheader(f"Profile — {selected}")
        st.write(profile)
        col1, col2 = st.columns([2,1])
        with col1:
            notes = st.text_area("Optional notes / constraints")
            if st.button("Generate Plan (rule-based)"):
                calories = estimate_calories(profile["weight"], profile["goal"])
                split = suggest_split(profile["gym_days"])
                workout = build_workout(profile["goal"], profile["gym_days"], profile["experience"])
                meals = build_meal_plan(profile["diet"], calories)
                plan = {"generated_at": str(datetime.now()), "split":split, "workout":workout, "meals":meals, "calories":calories, "notes":notes}
                st.session_state["profiles"][selected]["latest_plan"] = plan
                st.success("Plan generated and saved in session.")
                st.rerun()

        with col2:
            st.subheader("Quick Preview")
            if "latest_plan" in profile:
                lp = profile["latest_plan"]
                st.metric("Calories (est.)", lp["calories"])
                st.markdown("**Split**: " + lp["split"])
                st.markdown("**Sample Meals**:")
                for m in lp["meals"]["meals"]:
                    st.write(f"- {m['time']}: {', '.join(m['items'])}")
                st.markdown("**Workout sample (first session)**")
                st.write(lp["workout"][0])
        if "latest_plan" in profile:
            with st.expander("View full saved plan"):
                st.json(profile["latest_plan"])

elif page == "Progress Log":
    st.header("Progress & Logs (session only)")
    profiles = list(st.session_state["profiles"].keys())
    if not profiles:
        st.warning("No profiles in session.")
    else:
        selected = st.selectbox("Choose profile to log progress", profiles)
        logs = st.session_state["logs"].get(selected, [])
        col1, col2 = st.columns(2)
        with col1:
            d = st.date_input("Date", value=date.today())
            weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=st.session_state["profiles"][selected]["weight"])
            mood = st.selectbox("Mood", options=["Great","Good","Okay","Tired","Stressed"], index=1)
            workout_done = st.checkbox("Completed today's planned workout?")
            notes = st.text_area("Notes (optional)")
            if st.button("Save Log"):
                entry = {"date": str(d), "weight": weight, "mood": mood, "workout_done":workout_done, "notes":notes}
                logs.append(entry)
                st.session_state["logs"][selected] = logs
                st.session_state["profiles"][selected]["weight"] = weight
                st.success("Log saved in session.")
                st.rerun()

        with col2:
            st.subheader("Recent logs")
            if logs:
                df = pd.DataFrame(logs)
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("date")
                st.line_chart(df.set_index("date")["weight"])
                for entry in df.sort_values("date", ascending=False).head(10).to_dict("records"):
                    st.write(f"{entry['date'].date()} — {entry['weight']}kg — {entry['mood']} — workout: {'Yes' if entry['workout_done'] else 'No'}")
            else:
                st.info("No logs yet. Add your first log!")

elif page == "About":
    st.header("About BALSHALA")
    st.markdown("""
    BALSHALA — AI Gym Coach (Streamlit demo). This app demonstrates a session-based implementation of the project synopsis:
    - Personalized workout & meal plan generation (rule-based templates)
    - Split scheduler and progression tips
    - Motivational quotes and progress logging (session-only)
    """)
    st.markdown("**How to run locally**")
    st.code("pip install streamlit pandas\nstreamlit run app.py\n")
