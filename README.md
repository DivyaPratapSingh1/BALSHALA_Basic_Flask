
# BALSHALA — AI Gym Coach (Streamlit Version)

This repository contains the Streamlit redevelopment of the BALSHALA project (a personalized AI-style gym coach demo). It is session-based (no file writes) and is prepared for immediate deployment to Streamlit Cloud or local use.

## Features
- Create profiles (name, age, weight, goal, diet, gym days, experience) — session-only storage.
- Rule-based workout plan generation and split suggestions.
- Culturally-aware sample meal plans.
- Motivational quote widget and progress logging (session-only).
- Clean single-file Streamlit app for easy review and deployment.

## How to run locally (Windows)
1. Install Python 3.8+ if not already installed.
2. Open Command Prompt and navigate to this repository folder.
3. Create a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the app:
   ```
   streamlit run app.py
   ```

## Deploy to Streamlit Cloud
1. Push this repository to GitHub (replace old Flask files as needed).
2. Go to https://share.streamlit.io and deploy a new app using this repo and `app.py` as the entry point.

## Contribution note
This repository replaces an earlier Flask-based implementation with a Streamlit single-file app for better portability and ease of deployment.
