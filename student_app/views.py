from functools import wraps
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from .models import Student
from .serializers import StudentSerializer
from .forms import StudentForm,SearchForm,RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


# Create your views here.

def is_admin(user):
    return user.is_staff

def is_user(user):
    return user.is_authenticated and not user.is_staff

def home(request):
    return render(request,"index.html")

def credentials(request):
    return render(request,"credentials.html")

@login_required
def dashboard(request):
    context = {
        "is_admin": request.user.is_staff
    }
    return render(request, "dashboard.html", context)

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Done Successfully")
            return redirect("login")
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request,"registration.html",context)

def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request,"login.html",context)

@require_POST
@login_required
def signout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect("login")

@admin_required
def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Student Added Successfully.")
            return redirect("students")
    else:
        form = StudentForm()

    context = { "form": form }

    return render(request,"create_student.html",context)

@login_required
def student_list(request):
    search_form = SearchForm(request.GET)
    students = Student.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data["query"]
        if query:
            students = students.filter(name__icontains=query)

    context = {"students": students, "search_form": search_form}
    return render(request, "student_list.html", context)

@login_required
def student_details(request,pk):
    student = get_object_or_404(Student,pk=pk)
    context = { "student": student }
    return render(request,"student_details.html",context)

@admin_required
def update_student(request,pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request,"Student Updated Successfully.")
            return redirect("students")
    else:
        form = StudentForm(instance=student)

    context = { "form": form }

    return render(request,"update_student.html",context)

@admin_required
@require_POST
def delete_student(request,pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "Student Deleted Successfully.")
    return redirect("students")

class StudentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer




