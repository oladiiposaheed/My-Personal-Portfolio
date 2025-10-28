from django.contrib import admin
from django.utils.html import format_html
from .models import ProjectCategory, Technology, Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']
    
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'project_count')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'project_count')
    search_fields = ('name',)
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'featured', 'published', 'created_at', 'preview_image')
    list_filter = ('category', 'status', 'featured', 'published', 'created_at')
    list_editable = ('status', 'featured', 'published')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)
    search_fields = ('title', 'description', 'detailed_description')
    readonly_fields = ('preview_image', 'created_at', 'updated_at')
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'technologies', 'status', 'featured', 'published')
        }),
        ('Content', {
            'fields': ('description', 'detailed_description', 'image', 'preview_image')
        }),
        ('Links & Dates', {
            'fields': ('github_url', 'live_demo_url', 'start_date', 'end_date')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "-"
    preview_image.short_description = 'Preview'

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'order', 'preview_image')
    list_editable = ('order',)
    list_filter = ('project',)
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.image.url)
        return "-"
    preview_image.short_description = 'Preview'