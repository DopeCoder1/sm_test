from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View

from mentor.forms import ExamForm
from quiz.models import Exam, Student
from user.decorators import has_roles
from user.forms import RegisterUserForm, LoginUserForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from user.models import User


def is_admin(user):
    return user.roles[0] == "ADMIN"


def m_user_register_request(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            is_admin = True
            User.objects.create_user(email, password, is_admin)
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("m_user_profile")
        return render(request, "mentor/signup.html", context={"form": form})
    form = RegisterUserForm()
    return render(request, "mentor/signup.html", context={"form": form})


class m_LoginUser(LoginView):
    template_name = "mentor/login.html"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return reverse("m_user_profile")


class m_LogoutUser(m_LoginUser):
    template_name = "mentor/login.html"


@user_passes_test(is_admin)
def m_user_profile_get_request(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        context = {
            "form": user,
            "roles": user.roles[0]
        }
        return render(request, "mentor/user_profile.html", context)


@user_passes_test(is_admin)
def m_user_profile_edit(request):
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
                return redirect("m_user_profile")
            return render(request, "mentor/profile_edit.html", {"form": form})
        user = User.objects.get(id=request.user.id)
        form = UserProfileForm(
            initial={"first_name": user.first_name, "last_name": user.last_name, "birthdate": user.birthdate})
        return render(request, "mentor/profile_edit.html", {"form": form})


@user_passes_test(is_admin)
def my_student_list(request):
    pass


@login_required(login_url="mentor_login/")
@user_passes_test(is_admin)
def add_exam(request):
    if request.method == "POST":
        form = ExamForm(request.POST)

        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.save()
            form.save()
            return redirect("m_list_exam")
    else:
        form = ExamForm()
    return render(request, "mentor/exam_create.html", {"form": form})


@login_required(login_url="mentor_login/")
@user_passes_test(is_admin)
def list_exam(request):
    exams = Exam.objects.filter(user=request.user)
    return render(request, "mentor/exam_list.html", {"exams": exams})


# @login_required(login_url="mentor_login/")
# @user_passes_test(is_admin)
# def edit_exam(request, pk):
#     exam = get_object_or_404(Exam, id=pk)
#     if request.method == "POST":
#         form = ExamForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data.get("name")
#             duration = form.cleaned_data.get("duration")
#             passing_percentage = form.cleaned_data.get("passing_percentage")
#             users = form.cleaned_data.get("users")
#             active = form.cleaned_data.get("active")
#             show_result = form.cleaned_data.get("show_result")
#             exam.name = name
#             exam.duration = duration
#             exam.passing_percentage = passing_percentage
#             exam.active = active
#             exam.show_result = show_result
#             exam.save()
#             form.save()
#             import pdb
#             pdb.set_trace()
#             return redirect("m_list_exam")
#     form = ExamForm(initial={"name": exam.name, "duration": exam.duration, "passing_percentage": exam.passing_percentage, "users": [i.id for i in exam.users.all()], "active": exam.active, "show_result": exam.show_result})
#     return render(request, "mentor/exam_edit.html", {"form": form})
#
# @login_required(login_url="mentor_login/")
# @user_passes_test(is_admin)
# def delete_exam(request, pk):
#     exam = get_object_or_404(Exam, id=pk)
#     if request.method == "DELETE":
#         exam.delete()
#         return redirect("m_list_exam")

