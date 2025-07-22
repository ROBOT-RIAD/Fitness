from django.db import models
from accounts.models import User
# Create your models here.


class HealthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    perfect_weight_kg = models.FloatField(help_text="Ideal body weight in kilograms")
    abdominal = models.FloatField(help_text="Abdominal skinfold measurement in mm")
    triceps = models.FloatField(help_text="Triceps skinfold measurement in mm")
    subscapular = models.FloatField(help_text="Subscapular skinfold measurement in mm")
    suprailiac = models.FloatField(help_text="Suprailiac skinfold measurement in mm")
    total_calories_per_day = models.IntegerField(help_text="Estimated daily caloric need")
    water_need_liters_per_day = models.FloatField(help_text="Daily water intake requirement in liters")
    sleep_need_hours_per_day = models.FloatField(help_text="Daily sleep requirement in hours")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"HealthProfile for {self.user.username}"