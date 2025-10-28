from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Project, ProjectCategory

def project_list(request):
    """
    List all projects with filtering and search functionality
    """
    # Get filter parameters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    # Start with all published projects
    projects = Project.objects.filter(published=True).select_related('category').prefetch_related('technologies')
    
    # Apply filters
    if category_slug and category_slug != 'all':
        try:
            category = ProjectCategory.objects.get(slug=category_slug, is_active=True)
            projects = projects.filter(category=category)
        except ProjectCategory.DoesNotExist:
            pass
    
    # Apply search
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(technologies__name__icontains=search_query)
        ).distinct()
    
    # Order projects
    projects = projects.order_by('-featured', '-created_at')
    
    # Get filter options
    categories = ProjectCategory.objects.filter(is_active=True)
    
    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query or '',
    }
    
    return render(request, 'projects/project_list.html', context)

def project_detail(request, slug):
    """
    Display details of a specific project
    """
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related('technologies', 'images'),
        slug=slug, 
        published=True
    )
    
    # Get related projects (same category, excluding current project)
    related_projects = Project.objects.filter(
        category=project.category, 
        published=True
    ).exclude(id=project.id).select_related('category')[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'projects/project_detail.html', context)