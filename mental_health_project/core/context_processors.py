from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def auth_forms(request):
    return {
        'login_form': AuthenticationForm(),
        'register_form': RegisterForm()
    }
