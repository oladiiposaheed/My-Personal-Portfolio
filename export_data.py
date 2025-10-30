# export_data.py
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'porfolio.settings')
django.setup()

from django.core import serializers
from core.models import Profile
from projects.models import Project
from certifications.models import Certification
from django.contrib.auth.models import User

def export_all_data():
    # Create directories
    os.makedirs('core/fixtures', exist_ok=True)
    os.makedirs('projects/fixtures', exist_ok=True)
    os.makedirs('certifications/fixtures', exist_ok=True)
    
    print("Exporting data...")
    
    # Export Profile data
    with open('core/fixtures/profiles.json', 'w', encoding='utf-8') as f:
        data = serializers.serialize('json', Profile.objects.all())
        f.write(data)
    
    # Export Projects data
    with open('projects/fixtures/projects.json', 'w', encoding='utf-8') as f:
        data = serializers.serialize('json', Project.objects.all())
        f.write(data)
    
    # Export Certifications data
    with open('certifications/fixtures/certifications.json', 'w', encoding='utf-8') as f:
        data = serializers.serialize('json', Certification.objects.all())
        f.write(data)
    
    # Export Users
    with open('core/fixtures/users.json', 'w', encoding='utf-8') as f:
        data = serializers.serialize('json', User.objects.all())
        f.write(data)
    
    print("✅ All data exported successfully!")

if __name__ == '__main__':
    export_all_data()