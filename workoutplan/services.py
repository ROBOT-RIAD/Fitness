import json
from datetime import date, timedelta

import openai
from django.conf import settings
from accounts.constants import FITNESS_GOALS, LIFESTYLE_HABITS
from .utils import get_display_label, get_display_list   # same helpers you used before

openai.api_key = settings.OPENAI_API_KEY




def build_workout_plan(profile, training_data, workouts_qs, days=15):
    daily_duration_limit = training_data.get("daily_duration_minutes")
    from datetime import date, timedelta
    import json

    workouts = [{
        "uid":  w.unique_id,
        "name": w.workout_name,
        "type": w.workout_type,
        "target": w.for_body_part,
        "duration": str(w.time_needed),
        "calories": float(w.calories_burn),
        "equipment": w.equipment_needed,
        "tag": w.tag,
        "benefits": w.benefits,
    } for w in workouts_qs]

    fitness_goals = get_display_list(profile.fitness_goals, FITNESS_GOALS)
    readable_lifestyle = get_display_label(profile.lifestyle_habits, LIFESTYLE_HABITS)

    profile_dict = {
        "fullname":            profile.fullname,
        "gender":              profile.gender,
        "dob":                 str(profile.date_of_birth),
        "weight":              profile.weight,
        "height":              profile.height,
        "fitness_level":       profile.fitness_level,
        "equipment_home":      profile.at_home,
        "equipment_gym":       profile.at_gym,
        "medical_conditions":  profile.medical_conditions,
        "injuries_discomfort": training_data.get("injuries_discomfort"),
        "goals":               fitness_goals,
        "lifestyle":           readable_lifestyle,
    }

    muscle_focus = {k: v for k, v in training_data.items()
                    if k in ["chest", "back", "shoulders", "biceps", "triceps",
                             "quadriceps", "hamstrings", "glutes",
                             "calves", "adductors", "lower_back"] and v}

    start_date = date.today()
    date_list = [(start_date + timedelta(days=i)).isoformat() for i in range(days)]

    workout_json = ',\n        '.join([
        '{"set_of": 3, "reps": 12, "workout_uid": "abc123"}'
    ])

    prompt = f"""
You are a certified strength & conditioning coach.

The user’s primary fitness goals are: {", ".join(fitness_goals)}.
They train in a style described as: {training_data.get("train")}.
Injuries or discomfort to avoid: {training_data.get("injuries_discomfort") or "none"}.
Muscle‑group focus (1 means high priority): {json.dumps(muscle_focus, indent=2)}.

Use these exact {days} dates for the workout plan:
{json.dumps(date_list, indent=2)}

Generate a {days}-day workout plan in JSON format. Each day should include:

Generate a {days}-day workout plan in JSON format. Each day should include:

- "date"
- "title": short workout title in English (e.g., "Upper Body Strength")
- "title_spanish": Spanish translation of the title
- "tags": comma-separated tags in English (e.g., "arms, strength")
- "tags_spanish": comma-separated Spanish translation (e.g., "brazos, fuerza")
- "workouts": list of 3–6 workouts (from the provided list), each with:
    - workout_uid
    - set_of
    - reps


✅ Format (return as JSON):
{{
  "workout_plan_name": "Short catchy title",
  "tags": "comma,separated,tags",
  "days": [
    {{
      "date": "YYYY-MM-DD",
      "title": "Upper Body Strength",
      "tags": "chest,arms,strength",
      "workouts": [
        {workout_json}
      ]
    }},
    ...
  ]
}}

User profile:
{json.dumps(profile_dict, indent=2)}

Available workouts (duration ≤ {daily_duration_limit} minutes):
{json.dumps(workouts[:200], indent=2)}
"""

    chat = openai.ChatCompletion.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful workout‑plan assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    response_json = json.loads(chat.choices[0].message.content)

    return {
        "workout_plan_name": response_json.get("workout_plan_name", f"{days}-Day AI Workout Plan"),
        "tags": response_json.get("tags", ""),
        "days": response_json["days"],
    }
