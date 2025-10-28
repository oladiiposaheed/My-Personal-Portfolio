from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class ProjectCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, null=True, default='fas fa-folder')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'
        ordering = ['order', 'name']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    @property
    def active_projects_count(self):
        return self.projects.filter(published=True).count()

class Technology(models.Model):
    name = models.CharField(max_length=120, unique=True)
    icon = models.CharField(max_length=60, blank=True)
    
    class Meta:
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    detailed_description = models.TextField()
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects')
    technologies = models.ManyToManyField(Technology, blank=True, related_name='projects')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='completed')
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='projects/main/', blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # SEO
    meta_description = models.CharField(max_length=255, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-featured', '-created_at']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Resize project main image before saving
        if self.image and not self._state.adding:
            try:
                from PIL import Image
                
                img = Image.open(self.image)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize to optimal project image size (800x600 max)
                max_size = (800, 600)
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
                print(f"Error processing project image: {e}")
                pass
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})
    
    @property
    def short_description(self):
        return self.description[:150] + '...' if len(self.description) > 150 else self.description
    
    def get_status_badge_class(self):
        """Get Bootstrap badge class for status"""
        status_classes = {
            'completed': 'bg-success',
            'in_progress': 'bg-warning',
            'planned': 'bg-info',
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    @property
    def duration(self):
        """Calculate project duration"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return f"{(delta.days // 30)} months"
        elif self.start_date:
            return "Ongoing"
        return "Not specified"
    
    @property
    def is_active(self):
        """Check if project is currently active"""
        if self.status == 'in_progress':
            return True
        return False
    
    def clean(self):
        """Validate model data"""
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")
    
    def get_technologies_list(self):
        """Get list of technology names"""
        return list(self.technologies.values_list('name', flat=True))

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'
        ordering = ['order']
        
    def save(self, *args, **kwargs):
        # Resize gallery images before saving
        if self.image and not self._state.adding:
            try:
                from PIL import Image
                
                img = Image.open(self.image)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize gallery images to optimal size (600x400 max)
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
                print(f"Error processing project gallery image: {e}")
                pass
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'Image for {self.project.title}'
    
    @property
    def filename(self):
        return self.image.name.split('/')[-1] if self.image else ""