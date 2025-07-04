from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import ROLE_CHOICES,GENDER,FITNESS_LEVEL,TRAINER_CHOICES,AT_HOME_EQUIPMENT,AT_GYM_EQUIPMENT,SPORTS_CHOICES,INTERESTED_WORKOUT,ROUTINE_DURATION,DIETARY_PREFERENCES,ALLERGIES,FOOD_PREFERENCE,MEDICAL_CONDITIONS,FITNESS_GOALS,LIFESTYLE_HABITS
import random
from multiselectfield import MultiSelectField
# Create your models here.


class User(AbstractUser):
    # extra field add
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default="user")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='media/user_images/', null=True, blank=True)
    fullname = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    abdominal = models.FloatField(null=True, blank=True)
    sacroiliac = models.FloatField(null=True, blank=True)
    subscapularis = models.FloatField(null=True, blank=True)
    triceps = models.FloatField(null=True, blank=True)

    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVEL, null=True, blank=True)
    trainer = models.CharField(max_length=30, choices=TRAINER_CHOICES, null=True, blank=True)

    at_home = MultiSelectField(choices=AT_HOME_EQUIPMENT, max_length=100, null=True, blank=True)
    at_gym = MultiSelectField(choices=AT_GYM_EQUIPMENT, max_length=100, null=True, blank=True)
    martial_arts = MultiSelectField(choices=SPORTS_CHOICES, max_length=100, null=True, blank=True)
    running = MultiSelectField(choices=SPORTS_CHOICES, max_length=100, null=True, blank=True)
    other_sports = MultiSelectField(choices=SPORTS_CHOICES, max_length=100, null=True, blank=True)

    train_duration = models.CharField(max_length=100, null=True, blank=True)
    interested_workout = models.CharField(max_length=50, choices=INTERESTED_WORKOUT, null=True, blank=True)
    injuries_discomfort = models.TextField(null=True, blank=True)

    routine_duration = models.CharField(max_length=20, choices=ROUTINE_DURATION, null=True, blank=True)
    dietary_preferences = models.CharField(max_length=30, choices=DIETARY_PREFERENCES, null=True, blank=True)
    allergies = MultiSelectField(choices=ALLERGIES, max_length=100, null=True, blank=True)
    food_preference = MultiSelectField(choices=FOOD_PREFERENCE, max_length=100, null=True, blank=True)
    medical_conditions = MultiSelectField(choices=MEDICAL_CONDITIONS, max_length=100, null=True, blank=True)
    fitness_goals = MultiSelectField(choices=FITNESS_GOALS, max_length=100, null=True, blank=True)
    lifestyle_habits = models.CharField(max_length=20, choices=LIFESTYLE_HABITS, null=True, blank=True)

    def __str__(self):
        return self.fullname if self.fullname else str(self.user) 
    




class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    otp= models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def save(self,*args, **kwargs):
        if not self.otp:
            self.otp = str(random.randint(1000,9999))
        super().save(*args,**kwargs)

    def __str__(self):
       return f"{self.user.email} - {self.otp}" 
    