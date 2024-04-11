"""
URL configuration for Hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name='base'),
    path('',views.HOME,name='home'),


    path('patient/add',views.ADD_PATIENT,name='add_patient'), 
    path('patient/all',views.ALL_PATIENT,name='all_patient'), 
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'), 
    path('appointment/add',views.ADD_APPOINTMENT,name='add_appointment'), 
    path('appointment/all',views.ALL_APPOINTMENT,name='all_appointment'), 
    path('doctor/add',views.ADD_DOCTOR,name='add_doctor'), 
    path('doctor/all',views.ALL_DOCTOR,name='all_doctor'), 
    path('get_doctors_by_department/', views.get_doctors_by_department, name='get_doctors_by_department'),
    path('Beds/Book',views.BOOK_BED,name='book_bed'), 
    path('view_assigned_patients/<str:bed_type>/', views.view_assigned_patients, name='view_assigned_patients'),
    path('view_assigned_patients/General/', views.view_assigned_patients, name='view_assigned_patients/G'),
    path('release_patient/<int:patient_id>/', views.release_patient, name='release_patient'),

]
