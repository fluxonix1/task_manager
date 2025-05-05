from django import forms
from .models import Task
from .models import Comment
from .models import FileAttachment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

     

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class FileAttachmentForm(forms.ModelForm):
    class Meta:
        model = FileAttachment
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }