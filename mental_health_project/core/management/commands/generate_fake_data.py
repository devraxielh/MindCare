import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SurveyResponse
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Genera 1000 registros ficticios de encuestas de salud mental'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1000,
            help='Número de registros a generar (por defecto: 1000)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Crear usuarios ficticios si no existen
        self.stdout.write('Creando usuarios ficticios...')
        users = []
        for i in range(min(50, count)):  # Máximo 50 usuarios diferentes
            username = f'user_{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Usuario',
                    'last_name': f'{i+1}'
                }
            )
            users.append(user)
        
        self.stdout.write(f'Generando {count} registros de encuestas...')
        
        # Obtener las opciones de cada campo
        genders = [choice[0] for choice in SurveyResponse.GENDER_CHOICES]
        countries = [choice[0] for choice in SurveyResponse.COUNTRY_CHOICES]
        occupations = [choice[0] for choice in SurveyResponse.OCCUPATION_CHOICES]
        yes_no = [choice[0] for choice in SurveyResponse.YES_NO_CHOICES]
        yes_no_maybe = [choice[0] for choice in SurveyResponse.YES_NO_MAYBE_CHOICES]
        days_indoors = [choice[0] for choice in SurveyResponse.DAYS_INDOORS_CHOICES]
        mood_swings = [choice[0] for choice in SurveyResponse.MOOD_SWINGS_CHOICES]
        care_options = ['Not sure', 'No', 'Yes']
        
        # Generar registros
        responses = []
        for i in range(count):
            # Generar fecha aleatoria en los últimos 6 meses
            days_ago = random.randint(0, 180)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            # Crear respuesta con valores aleatorios
            response = SurveyResponse(
                user=random.choice(users),
                timestamp=timestamp,
                gender=random.choice(genders),
                country=random.choice(countries),
                occupation=random.choice(occupations),
                self_employed=random.choice(yes_no),
                family_history=random.choice(yes_no),
                treatment=random.choice(yes_no),
                days_indoors=random.choice(days_indoors),
                growing_stress=random.choice(yes_no_maybe),
                changes_habits=random.choice(yes_no_maybe),
                mental_health_history=random.choice(yes_no_maybe),
                mood_swings=random.choice(mood_swings),
                coping_struggles=random.choice(yes_no),
                work_interest=random.choice(yes_no_maybe),
                social_weakness=random.choice(yes_no_maybe),
                mental_health_interview=random.choice(yes_no_maybe),
                care_options=random.choice(care_options),
                prediction=random.choice(yes_no)  # Predicción aleatoria
            )
            responses.append(response)
            
            # Insertar en lotes de 100 para mejor rendimiento
            if (i + 1) % 100 == 0:
                SurveyResponse.objects.bulk_create(responses)
                responses = []
                self.stdout.write(f'  Creados {i + 1}/{count} registros...')
        
        # Insertar los registros restantes
        if responses:
            SurveyResponse.objects.bulk_create(responses)
        
        total = SurveyResponse.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Completado! Se generaron {count} registros ficticios.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'  Total de registros en la base de datos: {total}'
            )
        )
