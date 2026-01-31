"""
Views for the users application.
Handles user authentication, registration, role selection, and profile viewing logic.
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import SimpleUserRegistrationForm
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()


def landing_page(request):
    """Log out the current user and redirect to the login page."""
    logout(request)
    return redirect("login")


def register(request):
    """
    Handle user registration with support for multiple roles.

    Allows an existing user to register additional roles if credentials match,
    or creates a new user with the selected role.
    """
    form = SimpleUserRegistrationForm(request.POST or None)
    if request.method == "POST":
        role = request.POST.get("role")
        username = request.POST.get("username")
        password = request.POST.get("password1")

        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            if existing_user.check_password(password):
                role_field = f"is_{role}"
                if getattr(existing_user, role_field):
                    messages.error(request, "already existing")
                else:
                    setattr(existing_user, role_field, True)
                    existing_user.role = role
                    existing_user.save()
                    login(request, existing_user)
                    messages.success(request, f"Successfully registered as {role.capitalize()} and logged in!")
                    return redirect("article-list")
            else:
                messages.error(request, "Username taken or details incorrect.")
        else:
            if form.is_valid():
                user = form.save(commit=False)
                setattr(user, f"is_{role}", True)
                user.role = role
                user.save()
                login(request, user)
                messages.success(request, f"Registered as {role.capitalize()} and logged in!")
                return redirect("article-list")

    return render(request, "users/register.html", {"form": form})


def custom_login(request):
    """
    Authenticate a user and validate the selected role before login.

    Ensures that the user is registered for the chosen role before granting access.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user_record = User.objects.filter(username=username).first()
        if not user_record:
            messages.error(request, "username does not exist")
        else:
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "username or password incorrect, please try again")
            else:
                if role and role in user.registered_roles:
                    user.role = role
                    user.save(update_fields=["role"])
                    login(request, user)
                    messages.success(request, f"Logged in as {role.capitalize()}.")
                    return redirect("article-list")
                else:
                    messages.error(request, f"You are not registered as a {role.capitalize()}.")

    return render(
        request,
        "users/login.html",
        {
            "form": AuthenticationForm(),
            "roles": [("reader", "Reader"), ("journalist", "Journalist"), ("editor", "Editor")],
        },
    )


def get_user_roles(request):
    """
    Return the roles associated with a given username.

    Used by the frontend to dynamically display available roles.
    """
    username = request.GET.get("username")
    user = User.objects.filter(username=username).first()
    if user:
        return JsonResponse({"roles": user.registered_roles})
    return JsonResponse({"roles": []})


@csrf_exempt
def verify_credentials(request):
    """
    Verify user credentials and return available roles.

    Used by AJAX requests to validate login details before role selection.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "username does not exist"})

        user = authenticate(username=username, password=password)
        if user:
            return JsonResponse(
                {
                    "success": True,
                    "roles": user.registered_roles,
                    "role_names": {r: r.capitalize() for r in user.registered_roles},
                }
            )
        return JsonResponse(
            {
                "success": False,
                "error": "username or password incorrect, please try again",
            }
        )

    return JsonResponse({"success": False, "error": "Invalid request"})
