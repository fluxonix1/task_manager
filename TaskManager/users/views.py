from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user but don't commit to database yet
            user = form.save(commit=False)
            # You can set additional user attributes here if needed
            user.save()
            
            # Get username and password for automatic login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Authenticate and login the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome to TaskManager, {username}! Your account has been created successfully.')
                # Redirect to dashboard
                return redirect('dashboard')
            else:
                messages.warning(request, f'Account created for {username}, but automatic login failed. Please log in manually.')
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@require_http_methods(["GET"])
def custom_logout(request):
    try:
        # Store a message before logout
        messages.success(request, "You have been successfully logged out.")
        # Perform the logout
        logout(request)
        # Render the logout confirmation page instead of redirecting
        return render(request, 'users/logout.html')
    except Exception as e:
        # If there's an error, log it and redirect to login
        print(f"Logout error: {str(e)}")
        messages.error(request, f"There was an error during logout. Please try again.")
        return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Check if a new profile picture was uploaded
            if 'profile_picture' in request.FILES:
                # Save the form with the new profile picture
                user = form.save()
                messages.success(request, 'Your profile picture has been updated successfully!')
            else:
                # Save the form without changing the profile picture
                user = form.save()
                messages.success(request, 'Your profile information has been updated successfully!')
            
            return redirect('profile')
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form and try again.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    # Get completed tasks count
    try:
        from tasks.models import Task
        completed_tasks_count = Task.objects.filter(assigned_to=request.user, completed=True).count()
    except Exception as e:
        print(f"Error counting completed tasks: {str(e)}")
        completed_tasks_count = 0
    
    context = {
        'form': form,
        'title': 'My Profile',
        'completed_tasks_count': completed_tasks_count
    }
    return render(request, 'users/profile.html', context)
