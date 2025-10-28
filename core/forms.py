from django import forms
from core.models import ContactMessage

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
             
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': True
            }),
             
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required")
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name is required")
        return name