from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class Certification(models.Model):
    ISSUER_CHOICES = [
        ('coursera', 'Coursera'),
        ('edx', 'edX'),
        ('udacity', 'Udacity'),
        ('linkedin_learning', 'LinkedIn Learning'),
        ('deeplearning-ai', 'DeepLearning.AI'),
        ('google', 'Google'),
        ('microsoft', 'Microsoft'),
        ('aws', 'AWS'),
        ('ibm', 'IBM'),
        ('other', 'Other'),
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    issuer = models.CharField(max_length=50, choices=ISSUER_CHOICES)
    issuer_other = models.CharField(max_length=100, blank=True, null=True)
    certificate_id = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_url = models.URLField()
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    description = models.TextField()
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # SEO
    meta_description = models.CharField(max_length=255, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
        ordering = ['-issue_date', '-featured']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Resize certification image before saving
        if self.image and not self._state.adding:
            try:
                from PIL import Image
                
                img = Image.open(self.image)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize to optimal certification image size (600x400 max)
                max_size = (600, 400)
                if img.height > max_size[1] or img.width > max_size[0]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Save the resized image
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG', quality=85, optimize=True)
                    img_io.seek(0)
                    
                    # Replace the image field
                    self.image = InMemoryUploadedFile(
                        img_io,
                        'ImageField',
                        f"{os.path.splitext(self.image.name)[0]}.jpg",
                        'image/jpeg',
                        img_io.getbuffer().nbytes,
                        None
                    )
            except Exception as e:
                print(f"Error processing certification image: {e}")
                pass
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("certifications:certification_detail", kwargs={"slug": self.slug})

    def get_issuer_display_name(self):
        if self.issuer == 'other' and self.issuer_other:
            return self.issuer_other
        return self.get_issuer_display()
    
    @property
    def skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    @property
    def is_expired(self):
        """Check if certification is expired"""
        if self.expiration_date:
            return self.expiration_date < timezone.now().date()
        return False
    
    @property
    def days_until_expiry(self):
        """Calculate days until expiration"""
        if self.expiration_date:
            delta = self.expiration_date - timezone.now().date()
            return delta.days
        return None
    
    @property
    def is_expiring_soon(self):
        """Check if certification expires within 90 days"""
        if self.days_until_expiry and 0 < self.days_until_expiry <= 90:
            return True
        return False
    
    def get_level_badge_class(self):
        """Get Bootstrap badge class for level"""
        level_classes = {
            'beginner': 'bg-success',
            'intermediate': 'bg-info',
            'advanced': 'bg-warning',
            'expert': 'bg-danger',
        }
        return level_classes.get(self.level, 'bg-secondary')
    
    def get_issuer_icon(self):
        """Get FontAwesome icon for issuer"""
        issuer_icons = {
            'coursera': 'fas fa-graduation-cap',
            'edx': 'fas fa-university',
            'udacity': 'fas fa-laptop-code',
            'linkedin_learning': 'fab fa-linkedin',
            'deeplearning-ai': 'fas fa-brain',
            'google': 'fab fa-google',
            'microsoft': 'fab fa-microsoft',
            'aws': 'fab fa-aws',
            'ibm': 'fas fa-server',
            'other': 'fas fa-certificate',
        }
        return issuer_icons.get(self.issuer, 'fas fa-certificate')
    
    def clean(self):
        """Validate model data"""
        if self.expiration_date and self.expiration_date < self.issue_date:
            raise ValidationError("Expiration date cannot be before issue date.")
        
        if self.issuer == 'other' and not self.issuer_other:
            raise ValidationError("Please specify the issuer name when selecting 'Other'.")
    
    @property
    def status(self):
        """Get certification status"""
        if self.is_expired:
            return 'expired'
        elif self.is_expiring_soon:
            return 'expiring_soon'
        else:
            return 'valid'
    
    @property
    def years_since_issue(self):
        """Calculate years since certification was issued"""
        delta = timezone.now().date() - self.issue_date
        return delta.days // 365