from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from mentorlib.apps.users.models import User
# Create your views here.

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/users/login")

@requires_csrf_token
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            message = {
                "color":"red",
                "text":"Mot de passe ou nom d'utilisateur invalide"
            }
            return render(request, "users/login.html", context={"message":message})
    else:
        return render(request, "users/login.html")

@requires_csrf_token
def register_view(request):
    context = {
        "messages":[]
    }
    if request.method == "POST":
        user = User.objects.filter(email=request.POST["email"])
        if user:
            context['messages'].append({
                "color":"red",
                "text":"Un utilisateur est déjà inscrit avec ce mail"
            })
        else:
            user = User(
                email=request.POST["email"],
                first_name=request.POST["firstname"],
                last_name=request.POST["lastname"],
                username=request.POST["username"]
            )
            user.set_password(request.POST["password"])
            user.save()
            return redirect("/users/login")
        
        
    return render(request, "users/register.html", context=context)

def profile_view(request):
    return render(request, "users/profile.html")