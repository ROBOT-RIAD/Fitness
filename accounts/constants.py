# ROLE_CHOICES=(
#         ('admin', 'Admin'),
#         ('user', 'User'),
# )


# GENDER=(
#     ('male','Male'),
#     ('female','Female'),
# )


# FITNESS_LEVEL = (
#     ('Beginners', 'Beginners'),
#     ('Basic', 'Basic'),
#     ('Intermediate', 'Intermediate'),
#     ('High', 'High'),
# )

# TRAINER_CHOICES = (
#     ('At home', 'At Home'),
#     ('At gym', 'At Gym'),
#     ('Martial arts', 'Martial Arts'),
#     ('Running', 'Running'),
#     ('Other sports', 'Other Sports'),
# )

# AT_HOME_EQUIPMENT = (
#     ('Dumbbells', 'Dumbbells'),
#     ('Resistance bands', 'Resistance Bands'),
#     ('Pull-up bar', 'Pull-up Bar'),
#     ('Bench', 'Bench'),
#     ('No equipment', 'No Equipment'),
# )

# AT_GYM_EQUIPMENT = (
#     ('Barbell', 'Barbell'),
#     ('Squat rack', 'Squat Rack'),
#     ('Cable machine', 'Cable Machine'),
#     ('Smith machine', 'Smith Machine'),
# )

# SPORTS_CHOICES = (
#     ('Running', 'Running'),
#     ('Football', 'Football'),
#     ('Swimming', 'Swimming'),
# )

# INTERESTED_WORKOUT = (
#     ('Lose Fat', 'Lose Fat'),
#     ('Gain Muscle', 'Gain Muscle (only if % is already low)'),
#     ('Maintenance', 'Maintenance'),
# )

# ROUTINE_DURATION = (
#     ('1 Month', '1 Month'),
#     ('2 Month', '2 Month'),
#     ('3 Month', '3 Month'),
#     ('6 Month', '6 Month'),
#     ('1 Year', '1 Year'),
# )

# DIETARY_PREFERENCES = (
#     ('Keto', 'Keto'),
#     ('Paleo', 'Paleo'),
#     ('Vegetarian', 'Vegetarian'),
#     ('Vegan', 'Vegan'),
#     ('Gluten-Free', 'Gluten-Free'),
#     ('No preferences', 'No Preferences'),
# )

# ALLERGIES = (
#     ('Nuts', 'Nuts'),
#     ('Dairy', 'Dairy'),
#     ('Shellfish', 'Shellfish'),
#     ('Eggs', 'Eggs'),
#     ('No allergies', 'No Allergies'),
# )

# FOOD_PREFERENCE = (
#     ('Egg', 'Egg'),
#     ('Milk', 'Milk'),
#     ('Fish', 'Fish'),
# )

# MEDICAL_CONDITIONS = (
#     ('Diabetes', 'Diabetes'),
#     ('High blood pressure', 'High Blood Pressure'),
#     ('Heart disease', 'Heart Disease'),
# )

# FITNESS_GOALS = (
#     ('Weight loss', 'Weight Loss'),
#     ('Weight gain', 'Weight Gain'),
#     ('Maintenance', 'Maintenance'),
# )

# LIFESTYLE_HABITS = (
#     ('3 Meals', '3 Meals'),
#     ('4 Meals', '4 Meals'),
#     ('5 Meals', '5 Meals'),
#     ('6 Meals', '6 Meals'),
#     ('7 Meals', '7 Meals'),
#     ('8 Meals', '8 Meals'),
# )


from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = [
    ('admin', _('Admin')),
    ('user', _('User')),
]

GENDER = [
    ('male', _('Male')),
    ('female', _('Female')),
]

FITNESS_LEVEL = [
    ('Beginners', _('Beginners')),
    ('Basic', _('Basic')),
    ('Intermediate', _('Intermediate')),
    ('High', _('High')),
]

TRAINER_CHOICES = [
    ('At home', _('At Home')),
    ('At gym', _('At Gym')),
    ('Martial arts', _('Martial Arts')),
    ('Running', _('Running')),
    ('Other sports', _('Other Sports')),
]

AT_HOME_EQUIPMENT = [
    ('Dumbbells', _('Dumbbells')),
    ('Resistance bands', _('Resistance Bands')),
    ('Pull-up bar', _('Pull-up Bar')),
    ('Bench', _('Bench')),
    ('No equipment', _('No Equipment')),
]

AT_GYM_EQUIPMENT = [
    ('Barbell', _('Barbell')),
    ('Squat rack', _('Squat Rack')),
    ('Cable machine', _('Cable Machine')),
    ('Smith machine', _('Smith Machine')),
]

SPORTS_CHOICES = [
    ('Running', _('Running')),
    ('Football', _('Football')),
    ('Swimming', _('Swimming')),
]

INTERESTED_WORKOUT = [
    ('Lose Fat', _('Lose Fat')),
    ('Gain Muscle', _('Gain Muscle (only if % is already low)')),
    ('Maintenance', _('Maintenance')),
]

ROUTINE_DURATION = [
    ('1 Month', _('1 Month')),
    ('2 Month', _('2 Month')),
    ('3 Month', _('3 Month')),
    ('6 Month', _('6 Month')),
    ('1 Year', _('1 Year')),
]

DIETARY_PREFERENCES = [
    ('Keto', _('Keto')),
    ('Paleo', _('Paleo')),
    ('Vegetarian', _('Vegetarian')),
    ('Vegan', _('Vegan')),
    ('Gluten-Free', _('Gluten-Free')),
    ('No preferences', _('No Preferences')),
]

ALLERGIES = [
    ('Nuts', _('Nuts')),
    ('Dairy', _('Dairy')),
    ('Shellfish', _('Shellfish')),
    ('Eggs', _('Eggs')),
    ('No allergies', _('No Allergies')),
]

FOOD_PREFERENCE = [
    ('Egg', _('Egg')),
    ('Milk', _('Milk')),
    ('Fish', _('Fish')),
]

MEDICAL_CONDITIONS = [
    ('Diabetes', _('Diabetes')),
    ('High blood pressure', _('High Blood Pressure')),
    ('Heart disease', _('Heart Disease')),
]

FITNESS_GOALS = [
    ('Weight loss', _('Weight Loss')),
    ('Weight gain', _('Weight Gain')),
    ('Maintenance', _('Maintenance')),
]

LIFESTYLE_HABITS = [
    ('3 Meals', _('3 Meals')),
    ('4 Meals', _('4 Meals')),
    ('5 Meals', _('5 Meals')),
    ('6 Meals', _('6 Meals')),
    ('7 Meals', _('7 Meals')),
    ('8 Meals', _('8 Meals')),
]
