from django.contrib import admin
from django.utils.html import format_html
from .models import Certification

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'get_issuer_display_name', 
        'level', 
        'issue_date', 
        'expiration_date', 
        'featured',
        'is_active',
        'preview_image',
        'is_expired_display'
    )
    list_filter = ('issuer', 'level', 'featured', 'is_active', 'issue_date')
    list_editable = ('featured', 'is_active')
    search_fields = ('title', 'description', 'certificate_id', 'skills')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('preview_image', 'created_at', 'updated_at', 'is_expired_display')
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'issuer', 'issuer_other', 'level', 'featured', 'is_active')
        }),
        ('Certification Details', {
            'fields': ('certificate_id', 'issue_date', 'expiration_date', 'credential_url', 'image', 'preview_image')
        }),
        ('Description & Skills', {
            'fields': ('description', 'skills')
        }),
        ('Status', {
            'fields': ('is_expired_display',),
            'classes': ('collapse',)
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
    
    def get_issuer_display_name(self, obj):
        return obj.get_issuer_display_name()
    get_issuer_display_name.short_description = 'Issuer'
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: contain;" />', obj.image.url)
        return "-"
    preview_image.short_description = 'Preview'
    
    def is_expired_display(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red; font-weight: bold;">EXPIRED</span>')
        elif obj.expiration_date:
            days_left = obj.days_until_expiry
            if days_left < 30:
                return format_html('<span style="color: orange; font-weight: bold;">Expires in {} days</span>', days_left)
            else:
                return format_html('<span style="color: green;">Valid ({} days left)</span>', days_left)
        return format_html('<span style="color: green;">No expiration</span>')
    is_expired_display.short_description = 'Status'