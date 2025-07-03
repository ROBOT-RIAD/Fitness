ROLE_CHOICES=(
        ('admin', 'Admin'),
        ('user', 'User'),
)


GENDER=(
    ('male','Male'),
    ('female','Female'),
)


FITNESS_LEVEL = (
    ('Beginners', 'Beginners'),
    ('Basic', 'Basic'),
    ('Intermediate', 'Intermediate'),
    ('High', 'High'),
)

TRAINER_CHOICES = (
    ('At home', 'At Home'),
    ('At gym', 'At Gym'),
    ('Martial arts', 'Martial Arts'),
    ('Running', 'Running'),
    ('Other sports', 'Other Sports'),
)

AT_HOME_EQUIPMENT = (
    ('Dumbbells', 'Dumbbells'),
    ('Resistance bands', 'Resistance Bands'),
    ('Pull-up bar', 'Pull-up Bar'),
    ('Bench', 'Bench'),
    ('No equipment', 'No Equipment'),
)

AT_GYM_EQUIPMENT = (
    ('Barbell', 'Barbell'),
    ('Squat rack', 'Squat Rack'),
    ('Cable machine', 'Cable Machine'),
    ('Smith machine', 'Smith Machine'),
)

SPORTS_CHOICES = (
    ('Running', 'Running'),
    ('Football', 'Football'),
    ('Swimming', 'Swimming'),
)

INTERESTED_WORKOUT = (
    ('Lose Fat', 'Lose Fat'),
    ('Gain Muscle', 'Gain Muscle (only if % is already low)'),
    ('Maintenance', 'Maintenance'),
)

ROUTINE_DURATION = (
    ('1 Month', '1 Month'),
    ('2 Month', '2 Month'),
    ('3 Month', '3 Month'),
    ('6 Month', '6 Month'),
    ('1 Year', '1 Year'),
)

DIETARY_PREFERENCES = (
    ('Keto', 'Keto'),
    ('Paleo', 'Paleo'),
    ('Vegetarian', 'Vegetarian'),
    ('Vegan', 'Vegan'),
    ('Gluten-Free', 'Gluten-Free'),
    ('No preferences', 'No Preferences'),
)

ALLERGIES = (
    ('Nuts', 'Nuts'),
    ('Dairy', 'Dairy'),
    ('Shellfish', 'Shellfish'),
    ('Eggs', 'Eggs'),
    ('No allergies', 'No Allergies'),
)

FOOD_PREFERENCE = (
    ('Egg', 'Egg'),
    ('Milk', 'Milk'),
    ('Fish', 'Fish'),
)

MEDICAL_CONDITIONS = (
    ('Diabetes', 'Diabetes'),
    ('High blood pressure', 'High Blood Pressure'),
    ('Heart disease', 'Heart Disease'),
)

FITNESS_GOALS = (
    ('Weight loss', 'Weight Loss'),
    ('Weight gain', 'Weight Gain'),
    ('Maintenance', 'Maintenance'),
)

LIFESTYLE_HABITS = (
    ('3 Meals', '3 Meals'),
    ('4 Meals', '4 Meals'),
    ('5 Meals', '5 Meals'),
    ('6 Meals', '6 Meals'),
    ('7 Meals', '7 Meals'),
    ('8 Meals', '8 Meals'),
)