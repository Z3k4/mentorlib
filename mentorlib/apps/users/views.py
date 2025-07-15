from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from mentorlib.apps.users.models import User, UserNote
from mentorlib.apps.configuration.models import Resource
from mentorlib.apps.users.forms import UserSettingsForm
from django.contrib.auth.hashers import check_password, make_password


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/users/login")


@requires_csrf_token
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            message = {
                "color": "red",
                "text": "Mot de passe ou nom d'utilisateur invalide",
            }
            return render(request, "users/login.html", context={"message": message})
    else:
        return render(request, "users/login.html")


@requires_csrf_token
def register_view(request):
    context = {"messages": []}
    if request.method == "POST":
        user = User.objects.filter(email=request.POST["email"])
        if user:
            context["messages"].append(
                {"color": "red", "text": "Un utilisateur est déjà inscrit avec ce mail"}
            )
        else:
            user = User(
                email=request.POST["email"],
                first_name=request.POST["firstname"],
                last_name=request.POST["lastname"],
                username=request.POST["username"],
            )
            user.set_password(request.POST["password"])
            user.save()
            return redirect("/users/login")

    return render(request, "users/register.html", context=context)


def profile_view(request, id):
    context = {"user": User.objects.get(id=id), "resources": Resource.objects.all()}
    return render(request, "users/profile.html", context=context)


@requires_csrf_token
def settings_view(request):
    context = {
        "form": UserSettingsForm(
            initial={
                "last_name": request.user.last_name,
                "first_name": request.user.first_name,
            }
        )
    }

    if request.method == "POST":
        user = User.objects.get(id=request.user.id)

        if request.POST["current_password"]:
            if request.POST["password"] and check_password(
                request.POST["current_password"], user.password
            ):
                user.password = make_password(request.POST["password"])

        if request.POST["last_name"]:
            user.last_name = request.POST["last_name"]

        if request.POST["first_name"]:
            user.first_name = request.POST["first_name"]

        user.save()

    return render(request, "users/settings.html", context=context)


@requires_csrf_token
def profile_note_view(request, id, resource_id):
    user = User.objects.get(id=id)
    context = {
        "user": user,
        "user_notes": UserNote.objects.filter(
            user__id=id, resource__id=resource_id
        ).order_by("-date"),
        "messages": [],
    }

    action = request.GET.get("action")

    if action == "delete":
        try:
            user_note_id = request.GET.get("user_note")
            user_note = UserNote.objects.get(id=user_note_id)

            # TODO: allows admin, or users that have the permission to remove
            if user_note.mentor == request.user:
                user_note.delete()
        except Exception:
            context["messages"].append({"text": "La note n'existe pas", "color": "red"})

    if request.method == "POST":
        if request.user != user or user.is_superuser:
            # User can't note himself
            note = request.POST["message"]
            new_note = UserNote(
                user=user,
                mentor=request.user,
                note=note,
                resource=Resource.objects.get(id=resource_id),
            )
            new_note.save()

    return render(request, "users/profile/edit_note.html", context=context)
