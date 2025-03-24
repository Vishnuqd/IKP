from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # New user is not approved by default
            user.save()
            login(request, user)  #  Log in the user after successful registration
            messages.success(request, "Account created successfully! Please wait for admin approval.")
            return redirect('home')  # Redirect to home page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_approved:
                messages.error(request, "Your account is pending approval by an admin.")
                return redirect('login')
            login(request, user)
            if user.role == 'admin':  # Check if the user's role is 'admin'
                return redirect('admin_dashboard')  # Redirect to Django admin panel
            elif user.role == 'faculty':  # Redirect to faculty dashboard
                return redirect('faculty_dashboard')
            elif user.role == 'student':  # Redirect to student dashboard
                return redirect('student_dashboard')
            else:
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')

@login_required
def student_dashboard(request):
    """Student Dashboard View"""
    if not request.user.is_approved:
        messages.error(request, "Your account is pending approval.")
        return redirect('home')
    return render(request, 'users/student_dashboard.html')

@login_required
def faculty_dashboard(request):
    """Faculty Dashboard View"""
    if not request.user.is_approved:
        messages.error(request, "Your account is pending approval.")
        return redirect('home')
    return render(request, 'users/faculty_dashboard.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to access this page.")
        return redirect('home')
    
    unapproved_users = CustomUser.objects.filter(is_approved=False)
    approved_users = CustomUser.objects.filter(is_approved=True)
    return render(request, 'users/admin_dashboard.html', {'unapproved_users': unapproved_users, 'approved_users': approved_users})

@login_required
def approve_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to approve users.")
        return redirect('home')

    user = CustomUser.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f"{user.username} has been approved.")
    return redirect('admin_dashboard')

@login_required
def reject_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to reject users.")
        return redirect('home')

    user = CustomUser.objects.get(id=user_id)
    user.delete()
    messages.success(request, f"{user.username} has been rejected and deleted.")
    return redirect('admin_dashboard')
