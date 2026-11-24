from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class StudentForm(forms.ModelForm):
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^\d{11}$",
                message="Phone number must contain exactly 11 digits."
            )
        ]
    )

    class Meta:
        model = Student
        fields = ["name","email","gpa","department","phone_number"]

    # def clean_email(self):
    #     email = self.cleaned_data["email"]

    #     if not "@" in email:
    #         raise forms.ValidationError("Email must contain @.")
    #     return email

    def clean_gpa(self):
        gpa = self.cleaned_data["gpa"]

        if gpa < 0 or gpa > 4:
            raise forms.ValidationError("GPA must be between 0 and 4.")
        return gpa

class SearchForm(forms.Form):
        query = forms.CharField(label="Enter Name",required=False)
