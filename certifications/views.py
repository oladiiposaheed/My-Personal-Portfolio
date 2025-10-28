from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Certification

def certification_list(request):
    """
    Display all certifications with filtering options
    """
    # Get filter parameters
    issuer = request.GET.get('issuer')
    level = request.GET.get('level')
    search_query = request.GET.get('q')
    
    # Start with all active certifications
    certifications = Certification.objects.filter(is_active=True)
    
    # Apply filters
    if issuer and issuer != 'all':
        certifications = certifications.filter(issuer=issuer)
    
    if level and level != 'all':
        certifications = certifications.filter(level=level)
    
    # Apply search
    if search_query:
        certifications = certifications.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(skills__icontains=search_query) |
            Q(issuer_other__icontains=search_query)
        )
    
    # Order certifications
    certifications = certifications.order_by('-featured', '-issue_date')
    
    # Get filter options
    issuer_choices = Certification.ISSUER_CHOICES
    level_choices = Certification.LEVEL_CHOICES
    
    context = {
        'certifications': certifications,
        'issuer_choices': issuer_choices,
        'level_choices': level_choices,
        'selected_issuer': issuer,
        'selected_level': level,
        'search_query': search_query or '',
    }
    
    return render(request, 'certifications/certification_list.html', context)

def certification_detail(request, slug):
    """
    Display details of a specific certification
    """
    certification = get_object_or_404(Certification, slug=slug, is_active=True)
    
    # Get related certifications (same issuer or level)
    related_certifications = Certification.objects.filter(
        is_active=True
    ).exclude(id=certification.id).filter(
        Q(issuer=certification.issuer) | Q(level=certification.level)
    )[:4]
    
    # Parse skills into list
    skills_list = certification.skills_list
    
    context = {
        'certification': certification,
        'related_certifications': related_certifications,
        'skills_list': skills_list,
    }
    
    return render(request, 'certifications/certification_detail.html', context)