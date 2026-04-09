from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Student

class LoginView(View):
    template_name = "stud_app/login.html"

    def get(self, request):
        return render(request, self.template_name, {"error": None})

    def post(self, request):
        error = None
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif len(username) < 3:
            error = "Username must be at least 3 characters"
        elif len(password) < 4:
            error = "Password must be at least 4 characters"
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect("get-stud")
            try:
                User.objects.get(username=username)
                error = "Invalid password"
            except User.DoesNotExist:
                error = "Username does not exist"

        return render(request, self.template_name, {"error": error})

class LogoutView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully")
        return redirect("login")

class SignupView(View):
    template_name = "stud_app/signup.html"

    def get(self, request):
        return render(request, self.template_name, {"error": None, "success": None})

    def post(self, request):
        error = None
        success = None
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not username:
            error = "Username is required"
        elif not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        elif not confirm_password:
            error = "Please confirm your password"
        elif len(username) < 3:
            error = "Username must be at least 3 characters"
        elif len(password) < 4:
            error = "Password must be at least 4 characters"
        elif password != confirm_password:
            error = "Passwords do not match"
        else:
            if User.objects.filter(username=username).exists():
                error = "Username already exists"
            elif User.objects.filter(email=email).exists():
                error = "Email already exists"
            else:
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.save()
                    success = "Account created successfully! Please login."
                    return redirect("login")
                except Exception as e:
                    error = f"Error creating account: {str(e)}"

        return render(request, self.template_name, {"error": error, "success": success})

class HomeView(View):
    def get(self, request):
        return render(request, "stud_app/index.html")

class StudentListView(View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, "stud_app/display.html", {"data": students})

class InsertStudentView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, "stud_app/add.html")

    def post(self, request):
        r = request.POST.get("roll")
        name = request.POST.get("name")
        subject = request.POST.get("sub")
        marks = request.POST.get("mks")
        Student(roll=r, s_name=name, subject=subject, marks=marks).save()
        return redirect("get-stud")

class UpdateStudentView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, pk):
        obj = Student.objects.get(roll=pk)
        return render(request, "stud_app/update.html", {"data": obj})

    def post(self, request, pk):
        obj = Student.objects.get(roll=pk)
        obj.roll = request.POST.get("roll")
        obj.s_name = request.POST.get("name")
        obj.subject = request.POST.get("sub")
        obj.marks = request.POST.get("mks")
        obj.save()
        return redirect("get-stud")

class DeleteStudentView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, pk):
        obj = Student.objects.get(roll=pk)
        obj.delete()
        return redirect("get-stud")
