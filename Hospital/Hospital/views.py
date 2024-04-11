from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from app.models import *
def BASE(request):
    return render(request,'base.html')

def HOME(request):
    return render(request,'home.html')

def ADD_PATIENT(request):
    if request.method == "POST":
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address') 


        patient = Patient(
            patient_Name = patient_name,
            date_of_birth = dob,
            age = age,
            phone = phone,
            gender = gender,
            email = email,
            address = address,
        )
        patient.save()

       
    return render(request, 'patients/add_patient.html')

def ALL_PATIENT(request):
    patients = Patient.objects.all()
    return render(request, 'patients/all_patients.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'patients/patient_detail.html', {'patient': patient, 'appointments': appointments})

def ADD_APPOINTMENT(request):
    patients = Patient.objects.all()
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        patient = Patient.objects.get(pk=patient_id)
        department = request.POST.get('department')
        appointment_date = request.POST.get('appointment_date')
        appointment_time_str = request.POST.get('appointment_time')
        appointment_time = datetime.strptime(appointment_time_str, '%H:%M:%S').time() 
        doctor_name = request.POST.get('doctor_name')

        appointment = Appointment(
            patient=patient,
            department=department,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            doctor_name=doctor_name,
            status = 'Pending',
        )
        appointment.save()
        

    return render(request, 'appointment/add_appointment.html', {'patients': patients})

def ALL_APPOINTMENT(request):
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        status = request.POST.get('status')
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment.status = status
        appointment.save()

    appointments = Appointment.objects.all().order_by('appointment_date', 'appointment_time')
    return render(request, 'appointment/all_appointment.html', {'appointments': appointments})



def ADD_DOCTOR(request):
    if request.method == 'POST':
        doctor_name = request.POST.get('Doctor-name')
        dob = request.POST.get('dob')
        department = request.POST.get('department')
        experience = request.POST.get('experience')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        doctor_details = request.POST.get('about-doctor')
        address = request.POST.get('address')
        

        doctor = Doctor(
            doctor_name=doctor_name,
            dob=dob,
            department=department,
            experience=experience,
            phone=phone,
            email=email,
            gender=gender,
            doctor_details=doctor_details,
            address=address,
            
        )
        doctor.save()
    
    return render(request, 'doctors/add_doctor.html')

def ALL_DOCTOR(request):
    doctors = Doctor.objects.all()
    department = request.GET.get('department')
    if department:
        doctors = doctors.filter(department=department)
    return render(request, 'doctors/all_doctors.html', {'doctors': doctors, 'selected_department': department})


def get_doctors_by_department(request):
    department = request.GET.get('department')
    doctors = Doctor.objects.filter(department=department).values('id', 'doctor_name')
    return JsonResponse(list(doctors), safe=False)



def BOOK_BED(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient')
        bed_type = request.POST.get('bed_type')

        patient = Patient.objects.get(pk=patient_id)
        bed = Bed.objects.get(bed_type=bed_type)

        # Check if there are available beds for the selected type
        if bed.available_beds > 0:
            # Create a new BedAssignment object to represent the assignment of the patient to the bed
            assignment = BedAssignment.objects.create(patient=patient, bed=bed)
            # Decrement available beds for the selected type
            bed.available_beds -= 1
            bed.save()
            # Optionally, you can associate the patient with the bed here if needed

    patients = Patient.objects.all()
    beds = Bed.objects.all()

    # Count available beds for each bed type
    available_beds_count = {}
    for bed in beds:
        available_beds_count[bed.bed_type] = bed.available_beds

    return render(request, 'Beds/Book_bed.html', {'patients': patients, 'beds': beds, 'available_beds_count': available_beds_count})

def view_assigned_patients(request, bed_type):
    assigned_patients = BedAssignment.objects.filter(bed__bed_type=bed_type).values_list('patient', flat=True)
    patients = Patient.objects.filter(id__in=assigned_patients)
    bed_types = Bed.objects.values_list('bed_type', flat=True).distinct()
    return render(request, 'Beds/view_assigned_patients.html', {'patients': patients, 'bed_type': bed_type, 'bed_types': bed_types})

def release_patient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    bed_assignment = BedAssignment.objects.get(patient=patient)
    bed_type = bed_assignment.bed.bed_type
    bed = Bed.objects.get(bed_type=bed_type)
    bed.available_beds += 1  # Increase available beds
    bed.save()
    bed_assignment.delete()  # Delete the bed assignment
    return redirect('view_assigned_patients', bed_type=bed_type)
