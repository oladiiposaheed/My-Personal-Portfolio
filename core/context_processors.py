from core.models import Profile

def profile_data(request):
    """Make profile data available across all templates"""
    try:
        # Get the first profile (you might want to adjust this logic)
        profile = Profile.objects.select_related('user').first()
    except Profile.DoesNotExist:
        profile = None
    except Exception as e:
        # Log error in development
        if __debug__:
            print(f"Error loading profile: {e}")
        profile = None
    
    return {'profile': profile}