from django import forms
from .models import Student, Employer, Job, Application

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['university', 'gpa', 'achievements', 'skills']

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'open_positions']



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }

