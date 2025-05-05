from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Call the parent save method first
        super().save(*args, **kwargs)
        
        # Process the profile picture if it exists
        if self.profile_picture:
            img_path = self.profile_picture.path
            
            # Check if the file exists (it might not if we're in a test environment)
            if os.path.exists(img_path):
                # Open the image using PIL
                img = Image.open(img_path)
                
                # Resize if too large
                max_size = (300, 300)
                if img.height > max_size[1] or img.width > max_size[0]:
                    img.thumbnail(max_size)
                    img.save(img_path)
                    
                # Ensure the image is in a web-friendly format
                if img.format not in ['JPEG', 'PNG']:
                    img = img.convert('RGB')
                    img.save(img_path, format='JPEG', quality=85)