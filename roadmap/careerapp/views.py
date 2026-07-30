from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import Career, UserRoadmap


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect("user_profile")
        except User.DoesNotExist:
            pass

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        user = User.objects.get(email=email,username=username)
        if user:
            return render(request, "register.html", {"error": "Email or Username already exists."})
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return redirect("login")

    return render(request, "register.html")


@login_required
def user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # example career logic (replace with your own)
            career = Career.objects.first()
            roadmap = UserRoadmap.objects.create(
                user=request.user,
                career=selected_career
            )
            return redirect("career")
    else:
        form = UserProfileForm()

    return render(request, "user_profile.html", {"form": form})


@login_required
def career(request):
    roadmap = UserRoadmap.objects.filter(user=request.user).last()
    return render(request, "career.html", {"roadmap": roadmap})


@login_required
def roadmap(request):
    roadmap = UserRoadmap.objects.filter(user=request.user).last()
    return render(request, "roadmap.html", {"roadmap": roadmap})
