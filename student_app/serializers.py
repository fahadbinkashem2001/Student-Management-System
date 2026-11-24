from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id","name","email","gpa","department","phone_number"]

    def validate_gpa(self, value):
        if value < 0 or value > 4:
            raise serializers.ValidationError("GPA must be between 0 and 4.")
        return value

    def validate_phone_number(self, value):
        if not (value.isdigit() and len(value) == 11):
            raise serializers.ValidationError("Phone number must contain exactly 11 digits.")
        return value