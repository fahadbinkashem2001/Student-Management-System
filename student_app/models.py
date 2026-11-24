from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length= 100)
    email = models.EmailField(max_length= 100)
    gpa = models.DecimalField(max_digits=3,decimal_places=2)
    department = models.CharField(max_length= 50)
    phone_number = models.CharField(max_length= 15)

    def __str__(self):
        return self.name
