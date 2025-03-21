from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth import get_user_model


User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            #Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  #Redirect to the home page after successful login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')