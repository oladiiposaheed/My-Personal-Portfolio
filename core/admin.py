from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from core.models import Profile, ContactMessage

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('title', 'bio', 'about_me', 'profile_image', 'resume', 
              'github_url', 'linkedin_url', 'twitter_url', 'portfolio_url',
              'email', 'phone', 'address', 'meta_description', 'meta_keywords')

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'email', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'title', 'email')
    list_filter = ('created_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)