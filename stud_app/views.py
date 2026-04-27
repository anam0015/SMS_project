from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Student   # ✅ import model

# Login page
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        
        # Format Validation
        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif len(username) < 3:
            error = "Username must be at least 3 characters"
        elif len(password) < 4:
            error = "Password must be at least 4 characters"
        else:
            # User Database Validation
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # User exists and password is correct
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect("get-stud")
            else:
                # Check if username exists
                try:
                    User.objects.get(username=username)
                    error = "Invalid password"
                except User.DoesNotExist:
                    error = "Username does not exist"
    
    context = {"error": error}
    return render(request, "stud_app/login.html", context)

# Logout page
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("login")

# Signup page
def signup_view(request):
    error = None
    success = None
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        
        # Validation
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
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                error = "Username already exists"
            elif User.objects.filter(email=email).exists():
                error = "Email already exists"
            else:
                # Create new user
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
    
    context = {"error": error, "success": success}
    return render(request, "stud_app/signup.html", context)

# Home page
def home_view(request):
    return render(request, "stud_app/index.html")


# Display all students
def get_all_student(request):
    db = Student.objects.all()
    context = {"data": db}
    return render(request, "stud_app/display.html", context)


@login_required
def insert_student(request):
    
    if request.method == "POST":
        r = (request.POST.get("roll"))
        name = (request.POST.get("name"))
        subject = (request.POST.get("sub"))
        marks = (request.POST.get("mks"))
        
        
        obj = Student(roll=r,s_name=name,subject=subject,marks=marks)
        obj.save()
        
        return redirect("/students/student/")
    
    return render(request, "stud_app/add.html")


# def update_view(request, pk):
#     obj = Student.objects.get(roll=pk)

#     if request.method == "POST":
#         obj.roll = request.POST.get("roll")
#         obj.s_name = request.POST.get("name")
#         obj.subject = request.POST.get("sub")
#         obj.marks = request.POST.get("mks")
        
#         obj.save()
#         return redirect("get-stud")   # ✅ go back to list page

#     context = {"data": obj}
#     return render(request, "stud_app/update.html", context)

@login_required
def update_view(request, pk):
    obj = Student.objects.get(roll=pk)

    if request.method == "POST":
        obj.roll = request.POST.get("roll")
        obj.s_name = request.POST.get("name")
        obj.subject = request.POST.get("sub")
        obj.marks = request.POST.get("mks")
        
        obj.save()
        return redirect("get-stud")

    context = {"data": obj}
    return render(request, "stud_app/update.html", context)


@login_required
def delete_view(request, pk):
    obj = Student.objects.get(roll=pk)
    obj.delete()
    return redirect("/students/student/")


# Search students by name or roll number
@login_required
def search_student(request):
    query = request.GET.get('q', '').strip()
    data = []
    search_performed = False
    
    if query:
        search_performed = True
        # Search by roll number (exact match) or name (case-insensitive)
        try:
            # Try to search by roll number first
            roll_search = Student.objects.filter(roll=int(query))
            data = roll_search if roll_search.exists() else Student.objects.filter(s_name__icontains=query)
        except ValueError:
            # If query is not a number, search by name only
            data = Student.objects.filter(s_name__icontains=query)
    
    context = {
        "data": data, 
        "query": query,
        "search_performed": search_performed
    }
    return render(request, "stud_app/search_results.html", context)
     