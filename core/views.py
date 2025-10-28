from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms import ContactForm
from projects.models import Project
from certifications.models import Certification
from core.models import Profile

def home(request):
    """Home page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    # Get top 6 featured and published projects ordered by published date
    featured_projects = Project.objects.filter(featured=True, published=True).select_related('category')[:6] 
    
    # Get top 3 featured and active certifications ordered by issue date
    certifications = Certification.objects.filter(featured=True, is_active=True).order_by('-issue_date')[:3]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'certifications': certifications,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    context = {'profile': profile}
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
        
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('core:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'core/contact.html', context)