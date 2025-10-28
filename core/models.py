from django.db import models
from django.contrib.auth.models import User
import os
from django.core.files.storage import default_storage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=250, help_text='Your professional title', blank=True, default='Full Stack AI Engineer')
    bio = models.TextField(help_text='A short bio about yourself', blank=True, default='Passionate about building intelligent solutions that solve real-world problems.')
    about_me = models.TextField(help_text='Detailed information about you', blank=True, default='I specialize in creating end-to-end AI solutions that are scalable, maintainable, and user-friendly.')
    
    # Professional image field with resizing
    profile_image = models.ImageField(
        upload_to='profile/', 
        blank=True, 
        null=True,
        help_text='Upload a professional profile picture (will be resized to 400x400)'
    )
    
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    
    # Social Links
    github_url = models.URLField(blank=True, default='', verbose_name='GitHub URL')
    linkedin_url = models.URLField(blank=True, default='', verbose_name='LinkedIn URL')
    twitter_url = models.URLField(blank=True, default='', verbose_name='Twitter URL')
    portfolio_url = models.URLField(blank=True, default='', verbose_name='Portfolio URL')
    
    # Contact Information
    email = models.EmailField(help_text='Your professional email', blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    
    # SEO
    meta_description = models.CharField(max_length=255, blank=True, default='')
    meta_keywords = models.CharField(max_length=255, blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        if self.user.get_full_name():
            return f"{self.user.get_full_name()}'s Profile"
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        # Resize profile image before saving
        if self.profile_image and not self._state.adding:
            try:
                from PIL import Image
                
                # Open the image
                img = Image.open(self.profile_image)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize to professional size (400x400)
                if img.height > 400 or img.width > 400:
                    output_size = (400, 400)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                    
                    # Save the resized image
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG', quality=85, optimize=True)
                    img_io.seek(0)
                    
                    # Replace the image field
                    self.profile_image = InMemoryUploadedFile(
                        img_io,
                        'ImageField',
                        f"{os.path.splitext(self.profile_image.name)[0]}.jpg",
                        'image/jpeg',
                        img_io.getbuffer().nbytes,
                        None
                    )
            except Exception as e:
                # If there's an error with image processing, continue without resizing
                print(f"Error processing image: {e}")
                pass
        
        super().save(*args, **kwargs)

    @property
    def get_profile_image_url(self):
        """Get profile image URL with fallback"""
        if self.profile_image and hasattr(self.profile_image, 'url'):
            try:
                return self.profile_image.url
            except:
                pass
        return '/static/images/default-profile.jpg'

    # Helper methods for template checks
    def has_social_links(self):
        return any([self.github_url, self.linkedin_url, self.twitter_url, self.portfolio_url])
    
    def display_name(self):
        return self.user.get_full_name() or self.user.username


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"