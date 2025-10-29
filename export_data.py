import os
import django
import json
from django.core import serializers

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'porfolio.settings')
django.setup()

from core.models import *
from projects.models import *
from certifications.models import *
from django.contrib.auth.models import User

def export_data():
    # Create fixture directories if they don't exist
    os.makedirs('core/fixtures', exist_ok=True)
    os.makedirs('projects/fixtures', exist_ok=True)
    os.makedirs('certifications/fixtures', exist_ok=True)
    
    print("Starting data export...")

    try:
        # Export Core data (Profile)
        print("Exporting Profile data...")
        core_data = serializers.serialize('json', Profile.objects.all())
        with open('core/fixtures/core_data.json', 'w', encoding='utf-8') as f:
            f.write(core_data)
            
        # Export Projects data
        print("Exporting Projects data...")
        projects_data = serializers.serialize('json', Project.objects.all())
        with open('projects/fixtures/projects_data.json', 'w', encoding='utf-8') as f:
            f.write(projects_data)
        
        # Export Certifications data
        print("Exporting Certifications data...")
        certs_data = serializers.serialize('json', Certification.objects.all())
        with open('certifications/fixtures/certifications_data.json', 'w', encoding='utf-8') as f:
            f.write(certs_data)
            
        # Export Users
        print("Exporting Users data...")
        users_data = serializers.serialize('json', User.objects.all())
        with open('core/fixtures/users_data.json', 'w', encoding='utf-8') as f:
            f.write(users_data)
            
         
        print("✅ Data exported successfully!")
        print("Files created:")
        print(" - core/fixtures/core_data.json")
        print(" - projects/fixtures/projects_data.json")
        print(" - certifications/fixtures/certifications_data.json")
        print(" - core/fixtures/users_data.json")
        
    except Exception as e:
        print(f"❌ Error during export: {e}")
        
if __name__ == '__main__':
    export_data()