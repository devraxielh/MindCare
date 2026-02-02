from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RegisterForm, SurveyForm
from .models import SurveyResponse
from .ml_utils import predict_treatment
from django.db.models import Count

def home(request):
    return render(request, 'home.html')

def authors(request):
    return render(request, 'authors.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('survey')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('survey')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('survey')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('survey')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def survey(request):
    if request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            
            # Prepare data for prediction
            data = form.cleaned_data
            # Convert QueryDict/DB data to simple dict if needed (cleaned_data is dict)
            
            # Predict
            prediction = predict_treatment(data)
            response.prediction = prediction
            response.save()
            
            return redirect('results', response_id=response.id)
    else:
        form = SurveyForm()
    return render(request, 'survey.html', {'form': form})

@login_required
def results(request, response_id):
    # Allow admin to view results too if needed, or restricts? 
    # Usually admin needs to see details, so we allow superuser OR owner
    if request.user.is_superuser:
        response = SurveyResponse.objects.get(id=response_id)
    else:
        response = SurveyResponse.objects.get(id=response_id, user=request.user)
    return render(request, 'results.html', {'response': response})

@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    responses = SurveyResponse.objects.all()
    
    # 1. Filters
    gender_filter = request.GET.get('gender')
    country_filter = request.GET.get('country')
    prediction_filter = request.GET.get('prediction')
    
    if gender_filter:
        responses = responses.filter(gender=gender_filter)
    if country_filter:
        responses = responses.filter(country=country_filter)
    if prediction_filter:
        responses = responses.filter(prediction=prediction_filter)
    
    # 2. Statistics (on filtered data or all data? Usually user wants stats on filtered view or global stats separately. 
    # Let's show Global Stats + Filtered List. Or better, filtered stats.)
    
    total = responses.count()
    positive = responses.filter(prediction='Yes').count()
    negative = responses.filter(prediction='No').count()
    
    # Aggregates for Charts
    # Chart 1: Prediction Distribution (Pie)
    # Chart 2: Treatmean Needed by Gender (Bar)
    
    # Group by Gender -> Count of 'Yes' predictions
    # We can do this with aggregation or Python list comprehension if data is small. 
    # Using simple iteration for clarity as data is likely small for this demo.
    
    from collections import Counter
    
    # Gender Stats
    genders = responses.values_list('gender', flat=True)
    gender_counts = Counter(genders)
    gender_labels = list(gender_counts.keys())
    gender_data = list(gender_counts.values())
    
    # Treatment by Family History
    # We want: { 'Yes': count_treatment_yes, 'No': count_treatment_yes } (if we just want to see risk factor)
    # Let's show: % of people with Treatment=Yes grouped by FamilyHistory
    
    fam_hist_data = {}
    for choice in ['Yes', 'No']: # Family history choices
        subset = responses.filter(family_history=choice)
        total_sub = subset.count()
        if total_sub > 0:
            yes_count = subset.filter(prediction='Yes').count()
            fam_hist_data[choice] = (yes_count / total_sub) * 100
        else:
            fam_hist_data[choice] = 0
            
    fam_hist_labels = list(fam_hist_data.keys())
    fam_hist_values = list(fam_hist_data.values())

    # Calculate stats for ALL questions dynamically
    question_fields = [
        'self_employed', 'family_history', 'treatment', 'days_indoors', 
        'growing_stress', 'changes_habits', 'mental_health_history', 'mood_swings', 
        'coping_struggles', 'work_interest', 'social_weakness', 'mental_health_interview', 
        'care_options', 'occupation'
    ]
    
    question_stats = {}
    for field in question_fields:
        # Get verbose name
        field_obj = SurveyResponse._meta.get_field(field)
        verbose_name = field_obj.verbose_name
        
        # Get counts
        # We want a dictionary: { 'Label': Count, ... }
        # values_list returns tuples, Counter counts them
        values = responses.values_list(field, flat=True)
        counts = Counter(values)
        
        # Prepare data for Chart.js
        labels = list(counts.keys())
        data = list(counts.values())
        
        question_stats[field] = {
            'verbose_name': verbose_name,
            'labels': labels,
            'data': data,
            'id': f"chart_{field}" # Unique ID for canvas
        }

    # Get unique values for filters
    all_genders = SurveyResponse.objects.values_list('gender', flat=True).distinct()
    all_countries = SurveyResponse.objects.values_list('country', flat=True).distinct()

    # Pagination for responses table
    responses_list = responses.order_by('-timestamp')
    paginator = Paginator(responses_list, 20)  # 20 responses per page
    page = request.GET.get('page')
    
    try:
        paginated_responses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_responses = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        paginated_responses = paginator.page(paginator.num_pages)

    # Context
    context = {
        'total': total,
        'positive': positive,
        'negative': negative,
        'responses': paginated_responses,
        'gender_labels': gender_labels,
        'gender_data': gender_data,
        'fam_hist_labels': fam_hist_labels,
        'fam_hist_values': fam_hist_values,
        'all_genders': all_genders,
        'all_countries': all_countries,
        'current_filters': {
            'gender': gender_filter,
            'country': country_filter,
            'prediction': prediction_filter
        },
        'question_stats': question_stats # Pass the dynamic stats
    }
    return render(request, 'dashboard.html', context)

@login_required
def history(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    responses = SurveyResponse.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'history.html', {'responses': responses})

# User Management Views
@user_passes_test(lambda u: u.is_superuser)
def user_management(request):
    from django.contrib.auth.models import User
    
    # Get all users
    users_list = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = users_list.filter(
            username__icontains=search_query
        ) | users_list.filter(
            email__icontains=search_query
        ) | users_list.filter(
            first_name__icontains=search_query
        ) | users_list.filter(
            last_name__icontains=search_query
        )
    
    # Pagination
    paginator = Paginator(users_list, 20)
    page = request.GET.get('page')
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'user_management.html', context)

@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    from django.contrib.auth.models import User
    from .forms import UserEditForm
    from django.contrib import messages
    
    user_to_edit = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            # Prevent admin from removing their own admin status
            if user_to_edit.id == request.user.id and not form.cleaned_data['is_superuser']:
                messages.error(request, 'No puedes quitarte tu propio rol de administrador.')
            else:
                form.save()
                messages.success(request, f'Usuario {user_to_edit.username} actualizado exitosamente.')
                return redirect('user_management')
    else:
        form = UserEditForm(instance=user_to_edit)
    
    context = {
        'form': form,
        'user_to_edit': user_to_edit,
    }
    return render(request, 'edit_user.html', context)

@user_passes_test(lambda u: u.is_superuser)
def toggle_user_role(request, user_id):
    from django.contrib.auth.models import User
    from django.http import JsonResponse
    
    if request.method == 'POST':
        user_to_toggle = User.objects.get(id=user_id)
        
        # Prevent admin from removing their own admin status
        if user_to_toggle.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'No puedes cambiar tu propio rol de administrador.'
            })
        
        # Toggle the superuser status
        user_to_toggle.is_superuser = not user_to_toggle.is_superuser
        user_to_toggle.is_staff = user_to_toggle.is_superuser  # Keep staff status in sync
        user_to_toggle.save()
        
        return JsonResponse({
            'success': True,
            'is_superuser': user_to_toggle.is_superuser,
            'username': user_to_toggle.username
        })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
