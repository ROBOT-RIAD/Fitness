from django.db import models

# Create your models here.



class Workout(models.Model):
    unique_id = models.CharField(max_length=100, unique=True,null=True, blank=True,help_text="same WorkoutSpanish data")
    workout_name = models.CharField(max_length=255)
    time_needed = models.DurationField(help_text="Format: hh:mm:ss")
    for_body_part = models.CharField(max_length=100)  # Example: Chest, Legs, Full Body
    workout_type = models.CharField(max_length=100)   # Example: Strength, Cardio, HIIT
    calories_burn = models.DecimalField(max_digits=6, decimal_places=2)
    equipment_needed = models.CharField(max_length=200, blank=True)  # Example: Dumbbells, None
    tag = models.CharField(max_length=200, blank=True)               # Example: Fat Burn, Beginner
    image = models.ImageField(upload_to='media/workouts/', null=True, blank=True)
    benefits = models.TextField(help_text="List benefits separated by commas or lines.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Name: {self.workout_name}, "
            f"Type: {self.workout_type}, "
            f"Target: {self.for_body_part}, "
            f"Calories Burned: {self.calories_burn}, "
            f"Time: {self.time_needed}, "
            f"Equipment: {self.equipment_needed}, "
            f"Tag: {self.tag}, "
            f"Benefits: {self.benefits[:30]}..."
        )
    




class WorkoutSpanish(models.Model):
    unique_id = models.CharField(max_length=100, unique=True, null=True, blank=True,help_text="Same as related Workout object")
    workout_name = models.CharField(max_length=255)
    time_needed = models.DurationField(help_text="Formato: hh:mm:ss")
    for_body_part = models.CharField(max_length=100)  # Ejemplo: Pecho, Piernas, Cuerpo completo
    workout_type = models.CharField(max_length=100)   # Ejemplo: Fuerza, Cardio, HIIT
    calories_burn = models.DecimalField(max_digits=6, decimal_places=2)
    equipment_needed = models.CharField(max_length=200, blank=True)  # Ejemplo: Mancuernas, Ninguno
    tag = models.CharField(max_length=200, blank=True)               # Ejemplo: Quema Grasa, Principiante
    image = models.ImageField(upload_to='media/workouts/', null=True, blank=True)
    benefits = models.TextField(help_text="Lista de beneficios separados por comas o líneas.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Unique ID: {self.unique_id}, "
            f"Name: {self.workout_name}, "
            f"Type: {self.workout_type}, "
            f"Target: {self.for_body_part}, "
            f"Calories Burned: {self.calories_burn}, "
            f"Time: {self.time_needed}, "
            f"Equipment: {self.equipment_needed}, "
            f"Tag: {self.tag}, "
            f"Benefits: {self.benefits[:30]}..."
        )