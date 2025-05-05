from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from tasks.models import Task

# Custom admin for CustomUser
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'task_count', 'date_joined')
    
    def task_count(self, obj):
        return Task.objects.filter(assigned_to=obj).count()
    
    task_count.short_description = 'Task Count'

# Register CustomUser with our admin class
admin.site.register(CustomUser, CustomUserAdmin)
