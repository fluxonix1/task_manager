from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from datetime import date
from django.utils.timezone import now
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from .forms import FileAttachmentForm




@login_required
def dashboard(request):
    user = request.user
    tasks = Task.objects.filter(assigned_to=user)

    today = date.today()
    due_today = tasks.filter(due_date=today, completed=False)
    overdue = tasks.filter(due_date__lt=today, completed=False)

    context = {
        'user': user,
        'due_today': due_today,
        'overdue': overdue,
        'tasks': tasks,
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_list(request):
    user = request.user
    tasks = Task.objects.filter(assigned_to=user)

    # Filter
    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    # Sort
    sort = request.GET.get('sort')
    if sort == 'asc':
        tasks = tasks.order_by('due_date')
    elif sort == 'desc':
        tasks = tasks.order_by('-due_date')

    context = {
        'tasks': tasks,
        'status': status,
        'sort': sort,
    }
    return render(request, 'tasks/task_list.html', context)
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})




@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    comments = task.comments.all().order_by('-created_at')
    attachments = task.attachments.all().order_by('-uploaded_at')

    if request.method == 'POST':
        # Handle file upload
        if 'file_upload' in request.POST:
            file_form = FileAttachmentForm(request.POST, request.FILES)
            if file_form.is_valid():
                attachment = file_form.save(commit=False)
                attachment.task = task
                attachment.save()
                messages.success(request, "File uploaded successfully!")
                return redirect('task_detail', task_id=task.id)
        
        # Handle task status toggle
        elif 'toggle_status' in request.POST:
            task.completed = not task.completed
            task.save()
            status = "completed" if task.completed else "pending"
            messages.success(request, f"Task marked as {status}!")
            return redirect('task_detail', task_id=task.id)
        
        # Handle comment addition
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.user = request.user
                comment.save()
                messages.success(request, "Comment added successfully!")
                return redirect('task_detail', task_id=task.id)
    
    file_form = FileAttachmentForm()
    comment_form = CommentForm()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'file_form': file_form,
        'comment_form': comment_form,
        'comments': comments,
        'attachments': attachments,
    })
@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def user_profile(request):
    user = request.user
    tasks = Task.objects.filter(assigned_to=user)
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()
    
    # Check if UserProfile exists in the database schema
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks_userprofile';")
    table_exists = cursor.fetchone() is not None
    
    # If the table doesn't exist, we'll use a simplified context
    if not table_exists:
        context = {
            'user': user,
            'total_tasks': total,
            'completed_tasks': completed,
            'pending_tasks': pending,
            'profile_table_missing': True,
        }
    else:
        context = {
            'user': user,
            'total_tasks': total,
            'completed_tasks': completed,
            'pending_tasks': pending,
        }
    
    return render(request, 'tasks/profile.html', context)

@login_required
def update_profile(request):
    user = request.user
    
    # Check if UserProfile exists in the database schema
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks_userprofile';")
    table_exists = cursor.fetchone() is not None
    
    # If the table doesn't exist, we'll use a simplified approach
    if not table_exists:
        if request.method == 'POST':
            # Update user information only
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            
            # Save changes
            user.save()
            
            messages.success(request, "Basic profile information updated successfully!")
            return redirect('user_profile')
        
        context = {
            'user': user,
            'profile_table_missing': True,
        }
    else:
        # Normal flow when the profile table exists
        try:
            profile = user.profile
        except:
            # If the user doesn't have a profile yet, create one
            from tasks.models import UserProfile
            profile = UserProfile(user=user)
            profile.save()
        
        if request.method == 'POST':
            # Update user information
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            
            # Update profile information
            profile.bio = request.POST.get('bio', '')
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            
            # Save changes
            user.save()
            profile.save()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
        
        context = {
            'user': user,
            'profile': profile,
        }
    
    return render(request, 'tasks/update_profile.html', context)