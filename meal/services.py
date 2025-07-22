import json, datetime, openai
from django.conf import settings
from recipe.models import Recipe
from accounts.constants import FITNESS_GOALS, LIFESTYLE_HABITS
from .utils import get_display_label, get_display_list
openai.api_key = settings.OPENAI_API_KEY
from datetime import date, timedelta



def build_meal_plan(profile, recipes_qs, days=15):
    recipes = [{
        "uid": r.unique_id,
        "name": r.recipe_name,
        "cal": float(r.calories),
        "prot": float(r.protein),
        "carb": float(r.carbs),
        "fat": float(r.fat),
        "type": r.recipe_type,
        "for":  r.for_time,
        "tag":  r.tag,
    } for r in recipes_qs]

    fitness_goals = get_display_list(profile.fitness_goals, FITNESS_GOALS)
    readable_lifestyle = get_display_label(profile.lifestyle_habits, LIFESTYLE_HABITS)

    profile_dict = {
        "fullname":           profile.fullname,
        "gender":             profile.gender,
        "dob":                str(profile.date_of_birth),
        "weight":             profile.weight,
        "height":             profile.height,
        "dietary_preferences": profile.dietary_preferences,
        "medical_conditions":  profile.medical_conditions,
        "allergies":           profile.allergies,
        "fitness_goals":       profile.fitness_goals,
        "lifestyle_habits":    profile.lifestyle_habits,
    }

    # Map lifestyle habit to number of meals per day
    MEAL_COUNT_BY_LIFESTYLE = {
        '3 Meals': 3,
        '4 Meals': 4,
        '5 Meals': 5,
        '6 Meals': 6,
        '7 Meals': 7,
        '8 Meals': 8,
    }
    meal_count = MEAL_COUNT_BY_LIFESTYLE.get(readable_lifestyle, 3)

    # Define meal types up to 8 meals/day
    meal_types = [
        "Breakfast",
        "Snack"
        "Snack 1",
        "Lunch",
        "Snack 2",
        "Dinner",
        "Snack 3",
        "Post-Dinner",
        "Late Snack"
    ]
    
    meal_count = MEAL_COUNT_BY_LIFESTYLE.get(readable_lifestyle, 3)
    selected_meals = meal_types[:meal_count]

    # Build the JSON example for prompt (with placeholders)
    meal_json = ",\n        ".join([
    f'{{"meal_type": "{meal}", "recipe_uid": "abc123", "eating_time": "08:00"}}' for meal in selected_meals
])

    start_date = date.today()
    date_list = [(start_date + timedelta(days=i)).isoformat() for i in range(days)]

    prompt = f"""
You are a certified nutritionist.

The user has the following fitness goals: {", ".join(fitness_goals)}.
They prefer a routine of {readable_lifestyle.lower()} per day.

Use these exact {days} dates for the meal plan:
{json.dumps(date_list, indent=2)}

Generate a {days}-day meal plan using the provided recipes and user profile.

⚠️ IMPORTANT:
- Each day MUST include **Breakfast**, **Lunch**, and **Dinner**.
- You may add optional meals like snacks based on the user's lifestyle.
- Do NOT return any day that skips any of those three meals.
- ✅ Each meal entry MUST also include an `eating_time` in 24-hour format (HH:MM), appropriate to the meal type.

✅ Output format (MUST be valid JSON):
{{
  "meal_plan_name": "Short title like 'Muscle Gain Plan'",
  "tags": "comma,separated,tags",
  "days": [
    {{
      "date": "YYYY-MM-DD",
      "meals": [
        {meal_json}
      ]
    }},
    ...
  ]
}}

User profile (for reference):
{json.dumps(profile_dict, indent=2)}

Available recipes:
{json.dumps(recipes[:200], indent=2)}
"""

    chat = openai.ChatCompletion.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful meal-plan assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    response_json = json.loads(chat.choices[0].message.content)
    return {
        "meal_plan_name": response_json.get("meal_plan_name", f"{days}-Day AI Plan"),
        "tags": response_json.get("tags", ""),
        "days": response_json["days"]
    }