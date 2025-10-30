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
    
    print("Exporting local data to fixtures...")
    
    try:
        # Export Profile data
        profiles = Profile.objects.all()
        with open('core/fixtures/profiles.json', 'w', encoding='utf-8') as f:
            f.write(serializers.serialize('json', profiles))
        print(f"✅ Exported {len(profiles)} profiles")
        
        # Export Projects data
        projects = Project.objects.all()
        with open('projects/fixtures/projects.json', 'w', encoding='utf-8') as f:
            f.write(serializers.serialize('json', projects))
        print(f"✅ Exported {len(projects)} projects")
        
        # Export Certifications data
        certifications = Certification.objects.all()
        with open('certifications/fixtures/certifications.json', 'w', encoding='utf-8') as f:
            f.write(serializers.serialize('json', certifications))
        print(f"✅ Exported {len(certifications)} certifications")
        
        # Export Users
        users = User.objects.all()
        with open('core/fixtures/users.json', 'w', encoding='utf-8') as f:
            f.write(serializers.serialize('json', users))
        print(f"✅ Exported {len(users)} users")
        
        print("🎉 All local data exported successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    export_all_data()