from django.db import models

# Create your models here.

class Patient(models.Model):
    patient_Name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.patient_Name
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department_choices = [
        ('General', 'General'),
        ('Neuro', 'Neuro'),
        ('Ortho', 'Ortho'),
    ]
    department = models.CharField(max_length=50, choices=department_choices)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor_name = models.CharField(max_length=100)
    status_choices = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')

    def __str__(self):
        return f"{self.patient.patient_Name}'s Appointment"

    

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    DEPARTMENT_CHOICES = [
        ('General', 'General'),
        ('Ortho', 'Ortho'),
        ('Neuro', 'Neuro'),
    ]

    doctor_name = models.CharField(max_length=100)
    dob = models.DateField()
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    experience = models.IntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    doctor_details = models.TextField()
    address = models.TextField()
    

    def __str__(self):
        return self.doctor_name