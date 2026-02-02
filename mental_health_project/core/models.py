from django.db import models
from django.contrib.auth.models import User

class SurveyResponse(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Mujer'),
        ('Male', 'Hombre'),
    ]
    
    COUNTRY_CHOICES = [
        ('United States', 'Estados Unidos'), ('Poland', 'Polonia'), ('Australia', 'Australia'), 
        ('Canada', 'Canadá'), ('United Kingdom', 'Reino Unido'), ('South Africa', 'Sudáfrica'), 
        ('Sweden', 'Suecia'), ('New Zealand', 'Nueva Zelanda'), ('Netherlands', 'Países Bajos'), 
        ('India', 'India'), ('Belgium', 'Bélgica'), ('Ireland', 'Irlanda'), ('France', 'Francia'), 
        ('Portugal', 'Portugal'), ('Brazil', 'Brasil'), ('Costa Rica', 'Costa Rica'), 
        ('Russia', 'Rusia'), ('Germany', 'Alemania'), ('Switzerland', 'Suiza'), 
        ('Finland', 'Finlandia'), ('Israel', 'Israel'), ('Italy', 'Italia'), 
        ('Bosnia and Herzegovina', 'Bosnia y Herzegovina'), ('Singapore', 'Singapur'), 
        ('Nigeria', 'Nigeria'), ('Croatia', 'Croacia'), ('Thailand', 'Tailandia'), 
        ('Denmark', 'Dinamarca'), ('Mexico', 'México'), ('Greece', 'Grecia'), 
        ('Moldova', 'Moldavia'), ('Colombia', 'Colombia'), ('Georgia', 'Georgia'), 
        ('Czech Republic', 'República Checa'), ('Philippines', 'Filipinas')
    ]
    
    OCCUPATION_CHOICES = [
        ('Corporate', 'Corporativo'), ('Student', 'Estudiante'), ('Business', 'Negocios'), 
        ('Housewife', 'Ama de casa'), ('Others', 'Otros')
    ]
    
    YES_NO_CHOICES = [('Yes', 'Sí'), ('No', 'No')]
    YES_NO_MAYBE_CHOICES = [('Yes', 'Sí'), ('No', 'No'), ('Maybe', 'Tal vez')]
    
    DAYS_INDOORS_CHOICES = [
        ('1-14 days', '1-14 días'), 
        ('Go out Every day', 'Salgo todos los días'), 
        ('More than 2 months', 'Más de 2 meses'), 
        ('15-30 days', '15-30 días'), 
        ('31-60 days', '31-60 días')
    ]
    
    MOOD_SWINGS_CHOICES = [('Medium', 'Medio'), ('Low', 'Bajo'), ('High', 'Alto')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    
    # Feature fields
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name="Género")
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, verbose_name="País")
    occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, verbose_name="Ocupación")
    self_employed = models.CharField(max_length=50, choices=YES_NO_CHOICES, blank=True, null=True, verbose_name="Autónomo")
    family_history = models.CharField(max_length=50, choices=YES_NO_CHOICES, verbose_name="Historial Familiar")
    treatment = models.CharField(max_length=50, choices=YES_NO_CHOICES, blank=True, null=True, verbose_name="Tratamiento Previo")
    days_indoors = models.CharField(max_length=50, choices=DAYS_INDOORS_CHOICES, verbose_name="Días en Casa")
    growing_stress = models.CharField(max_length=50, choices=YES_NO_MAYBE_CHOICES, verbose_name="Aumento de Estrés")
    changes_habits = models.CharField(max_length=50, choices=YES_NO_MAYBE_CHOICES, verbose_name="Cambios de Hábitos")
    mental_health_history = models.CharField(max_length=50, choices=YES_NO_MAYBE_CHOICES, verbose_name="Historial de Salud Mental")
    mood_swings = models.CharField(max_length=50, choices=MOOD_SWINGS_CHOICES, verbose_name="Cambios de Humor")
    coping_struggles = models.CharField(max_length=50, choices=YES_NO_CHOICES, verbose_name="Dificultad para Afrontar Problemas")
    work_interest = models.CharField(max_length=50, choices=YES_NO_MAYBE_CHOICES, verbose_name="Interés en el Trabajo")
    social_weakness = models.CharField(max_length=50, choices=YES_NO_MAYBE_CHOICES, verbose_name="Debilidad Social")
    mental_health_interview = models.CharField(max_length=50, choices=YES_NO_MAYBE_CHOICES, verbose_name="Entrevista sobre Salud Mental")
    care_options = models.CharField(max_length=50, choices=[('Not sure', 'No estoy seguro'), ('No', 'No'), ('Yes', 'Sí')], verbose_name="Opciones de Cuidado")
    
    # Prediction result
    prediction = models.CharField(max_length=50, blank=True, null=True, verbose_name="Predicción") # "Yes" or "No" (Treatment needed)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
