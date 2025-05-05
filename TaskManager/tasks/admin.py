from django.contrib import admin
from .models import Task, FileAttachment, Comment
from users.models import CustomUser

# Customizing Task model in admin
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'assigned_to', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'

# Register Task model
admin.site.register(Task, TaskAdmin)

# Register other models
admin.site.register(FileAttachment)
admin.site.register(Comment)

# Customize User admin (if needed)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'task_count', 'date_joined')

    def task_count(self, obj):
        return Task.objects.filter(assigned_to=obj).count()
    
    task_count.short_description = 'Task Count'

# Register CustomUser model with our admin class in users/admin.py instead