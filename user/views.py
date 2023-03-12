from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from quiz.models import Student
from user.decorators import has_roles
from user.forms import RegisterUserForm, LoginUserForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from user.models import User

def is_user(user):
    return user.roles[0] == "USER"


def user_register_request(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            is_admin = False
            user_creation = User.objects.create_user(email, password, is_admin)
            student_creation = Student(user=user_creation)
            student_creation.save()
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_profile")
        return render(request, "user/signup.html", context={"form": form})
    form = RegisterUserForm()
    return render(request, "user/signup.html", context={"form": form})


class LoginUser(LoginView):
    template_name = "user/login.html"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return reverse("user_profile")

class LogoutUser(LoginUser):
    template_name = "user/login.html"

@user_passes_test(is_user)
def user_profile_get_request(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        context = {
            "form": user,
            "roles": user.roles[0]
        }
        return render(request, "user/user_profile.html", context)

@user_passes_test(is_user)
def user_profile_edit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                image = form.cleaned_data.get("image")
                birthdate = form.cleaned_data.get("birthdate")
                user = User.objects.get(id=request.user.id)
                user.first_name = first_name
                user.last_name = last_name
                user.image = image
                user.birthdate = birthdate
                user.save()
                return redirect("user_profile")
            return render(request, "user/profile_edit.html", {"form": form})
        user = User.objects.get(id=request.user.id)
        form = UserProfileForm(initial={"first_name": user.first_name, "last_name": user.last_name})
        return render(request, "user/profile_edit.html", {"form": form})
