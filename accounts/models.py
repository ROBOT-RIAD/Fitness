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
    



class ProfileSpanish(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_spanish')
    image = models.ImageField(upload_to='media/user_images/', null=True, blank=True)
    fullname = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nombre completo")
    gender = models.CharField(max_length=15, choices=(
        ('Masculino','Masculino'),
        ('Femenino','Femenino'),
    ), null=True, blank=True, verbose_name="Género")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")

    weight = models.FloatField(null=True, blank=True, verbose_name="Peso")
    height = models.FloatField(null=True, blank=True, verbose_name="Altura")
    abdominal = models.FloatField(null=True, blank=True, verbose_name="Abdominales")
    sacroiliac = models.FloatField(null=True, blank=True, verbose_name="Sacroilíaco")
    subscapularis = models.FloatField(null=True, blank=True, verbose_name="Subescapular")
    triceps = models.FloatField(null=True, blank=True, verbose_name="Tríceps")

    fitness_level = models.CharField(max_length=20, choices=(
        ('Principiante', 'Principiante'),
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ), null=True, blank=True, verbose_name="Nivel de forma física")

    trainer = models.CharField(max_length=30, choices=(
        ('En casa', 'En casa'),
        ('En el gimnasio', 'En el gimnasio'),
        ('Artes marciales', 'Artes marciales'),
        ('Correr', 'Correr'),
        ('Otros deportes', 'Otros deportes'),
    ), null=True, blank=True, verbose_name="Entrenador")

    at_home = MultiSelectField(choices=(
        ('Mancuernas', 'Mancuernas'),
        ('Bandas de resistencia', 'Bandas de resistencia'),
        ('Barra de dominadas', 'Barra de dominadas'),
        ('Banco', 'Banco'),
        ('Sin equipo', 'Sin equipo'),
    ), max_length=100, null=True, blank=True, verbose_name="Equipo en casa")

    at_gym = MultiSelectField(choices=(
        ('Barra', 'Barra'),
        ('Rack de sentadillas', 'Rack de sentadillas'),
        ('Máquina de cables', 'Máquina de cables'),
        ('Máquina Smith', 'Máquina Smith'),
    ), max_length=100, null=True, blank=True, verbose_name="Equipo en el gimnasio")

    martial_arts = MultiSelectField(choices=(
        ('Correr', 'Correr'),
        ('Fútbol', 'Fútbol'),
        ('Natación', 'Natación'),
    ), max_length=100, null=True, blank=True, verbose_name="Artes marciales")

    running = MultiSelectField(choices=(
        ('Correr', 'Correr'),
        ('Fútbol', 'Fútbol'),
        ('Natación', 'Natación'),
    ), max_length=100, null=True, blank=True, verbose_name="Correr")

    other_sports = MultiSelectField(choices=(
        ('Correr', 'Correr'),
        ('Fútbol', 'Fútbol'),
        ('Natación', 'Natación'),
    ), max_length=100, null=True, blank=True, verbose_name="Otros deportes")

    train_duration = models.CharField(max_length=100, null=True, blank=True, verbose_name="Duración del entrenamiento")

    interested_workout = models.CharField(max_length=50, choices=(
        ('Perder grasa', 'Perder grasa'),
        ('Ganar músculo', 'Ganar músculo'),
        ('Mantenimiento', 'Mantenimiento'),
    ), null=True, blank=True, verbose_name="Objetivo del entrenamiento")

    injuries_discomfort = models.TextField(null=True, blank=True, verbose_name="Lesiones o molestias")

    routine_duration = models.CharField(max_length=20, choices=(
        ('1 Mes', '1 Mes'),
        ('2 Meses', '2 Meses'),
        ('3 Meses', '3 Meses'),
        ('6 Meses', '6 Meses'),
        ('1 Año', '1 Año'),
    ), null=True, blank=True, verbose_name="Duración de la rutina")

    dietary_preferences = models.CharField(max_length=30, choices=(
        ('Keto', 'Keto'),
        ('Paleo', 'Paleo'),
        ('Vegetariano', 'Vegetariano'),
        ('Vegano', 'Vegano'),
        ('Sin gluten', 'Sin gluten'),
        ('Sin preferencias', 'Sin preferencias'),
    ), null=True, blank=True, verbose_name="Preferencias dietéticas")

    allergies = MultiSelectField(choices=(
        ('Nueces', 'Nueces'),
        ('Lácteos', 'Lácteos'),
        ('Mariscos', 'Mariscos'),
        ('Huevos', 'Huevos'),
        ('Sin alergias', 'Sin alergias'),
    ), max_length=100, null=True, blank=True, verbose_name="Alergias")

    food_preference = MultiSelectField(choices=(
        ('Huevo', 'Huevo'),
        ('Leche', 'Leche'),
        ('Pescado', 'Pescado'),
    ), max_length=100, null=True, blank=True, verbose_name="Preferencias alimenticias")

    medical_conditions = MultiSelectField(choices=(
        ('Diabetes', 'Diabetes'),
        ('Presión arterial alta', 'Presión arterial alta'),
        ('Enfermedad cardíaca', 'Enfermedad cardíaca'),
    ), max_length=100, null=True, blank=True, verbose_name="Condiciones médicas")

    fitness_goals = MultiSelectField(choices=(
        ('Pérdida de peso', 'Pérdida de peso'),
        ('Aumento de peso', 'Aumento de peso'),
        ('Mantenimiento', 'Mantenimiento'),
    ), max_length=100, null=True, blank=True, verbose_name="Objetivos de fitness")

    lifestyle_habits = models.CharField(max_length=20, choices=(
        ('3 comidas', '3 comidas'),
        ('4 comidas', '4 comidas'),
        ('5 comidas', '5 comidas'),
        ('6 comidas', '6 comidas'),
        ('7 comidas', '7 comidas'),
        ('8 comidas', '8 comidas'),
    ), null=True, blank=True, verbose_name="Hábitos alimenticios")

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
    