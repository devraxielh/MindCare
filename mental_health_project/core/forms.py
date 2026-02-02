from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SurveyResponse

class RegisterForm(UserCreationForm):
    pass


class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        exclude = ['user', 'timestamp', 'prediction']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'occupation': forms.Select(attrs={'class': 'form-control'}),
            'self_employed': forms.Select(attrs={'class': 'form-control'}),
            'family_history': forms.Select(attrs={'class': 'form-control'}),
            'treatment': forms.Select(attrs={'class': 'form-control'}),
            'days_indoors': forms.Select(attrs={'class': 'form-control'}),
            'growing_stress': forms.Select(attrs={'class': 'form-control'}),
            'changes_habits': forms.Select(attrs={'class': 'form-control'}),
            'mental_health_history': forms.Select(attrs={'class': 'form-control'}),
            'mood_swings': forms.Select(attrs={'class': 'form-control'}),
            'coping_struggles': forms.Select(attrs={'class': 'form-control'}),
            'work_interest': forms.Select(attrs={'class': 'form-control'}),
            'social_weakness': forms.Select(attrs={'class': 'form-control'}),
            'mental_health_interview': forms.Select(attrs={'class': 'form-control'}),
            'care_options': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'gender': 'Selecciona tu género. Esta información nos ayuda a personalizar mejor las recomendaciones.',
            'country': 'Indica el país donde resides actualmente. Esto puede influir en las opciones de atención disponibles.',
            'occupation': 'Tu ocupación actual. El tipo de trabajo puede estar relacionado con diferentes niveles de estrés.',
            'self_employed': '¿Trabajas por cuenta propia? Los trabajadores autónomos pueden enfrentar desafíos únicos de salud mental.',
            'family_history': '¿Algún miembro de tu familia ha sido diagnosticado con problemas de salud mental? El historial familiar puede ser un factor importante.',
            'treatment': '¿Has recibido tratamiento previo para problemas de salud mental? Esto incluye terapia, medicación o cualquier otro tipo de intervención.',
            'days_indoors': '¿Cuánto tiempo pasas en casa sin salir? El aislamiento prolongado puede afectar tu bienestar mental.',
            'growing_stress': '¿Has notado un aumento en tus niveles de estrés recientemente? Piensa en las últimas semanas o meses.',
            'changes_habits': '¿Has experimentado cambios significativos en tus hábitos diarios? Esto puede incluir cambios en el sueño, alimentación o rutinas.',
            'mental_health_history': '¿Tienes un historial personal de problemas de salud mental? Considera diagnósticos previos o episodios pasados.',
            'mood_swings': '¿Con qué frecuencia experimentas cambios bruscos de humor? Piensa en variaciones entre tristeza, irritabilidad y euforia.',
            'coping_struggles': '¿Te resulta difícil manejar situaciones estresantes o problemas cotidianos? Considera tu capacidad para afrontar desafíos.',
            'work_interest': '¿Has perdido interés en tu trabajo o actividades que antes disfrutabas? La pérdida de motivación puede ser un indicador importante.',
            'social_weakness': '¿Sientes dificultad para relacionarte con otras personas o mantener conexiones sociales? Considera tu nivel de comodidad en situaciones sociales.',
            'mental_health_interview': '¿Estarías dispuesto a participar en una entrevista sobre tu salud mental con un profesional? Esto ayudaría a obtener una evaluación más precisa.',
            'care_options': '¿Conoces las opciones de atención de salud mental disponibles para ti? Esto incluye acceso a terapia, servicios de apoyo o recursos comunitarios.',
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_active', 'is_superuser']
        labels = {
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'is_active': 'Usuario Activo',
            'is_superuser': 'Administrador'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
