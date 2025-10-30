import os
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'porfolio.settings')
    django.setup()
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Start server
    from django.core.management import call_command
    call_command('runserver', '0.0.0.0:8000')