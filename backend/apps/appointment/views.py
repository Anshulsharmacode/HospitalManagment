from django.shortcuts import render

from backend.apps.appointment.models import Appointment
from backend.apps.users.models import UserRole
from backend.common.api.api import success_response


def get_booked_slots(doctor_id, date):
    return Appointment.objects.filter(doctor_id=doctor_id, date=date, status__in=["PENDING", "CONFIRMED", "RESCHEDULED"]).values_list("time", flat=True)


ALL_SLOTS = [
    "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    "12:00", "12:30", "14:00", "14:30", "15:00", "15:30",
    "16:00", "16:30", "17:00",
]


def slot_available(doctor_id, date):
    booked_slots = get_booked_slots(doctor_id, date)
    return [slot for slot in ALL_SLOTS if slot not in booked_slots]


def slot(request):
    doctor_id = request.GET.get("doctor_id")
    date = request.GET.get("date")
    booked    = [str(t)[:5] for t in get_booked_slots(doctor_id, date)]
    available = [slot for slot in ALL_SLOTS if slot not in booked]

    return success_response({
        "doctor_id":       doctor_id,
        "date":            date,
        "booked_slots":    booked,
        "available_slots": available,
    })


def book_slot(request):

    doctor_id  = request.data.get("doctor")
    department = request.data.get("department")
    date       = request.data.get("date")
    time       = request.data.get("time")
    patient_id = request.data.get("patient")


    Appointment.objects.create(
        doctor_id=doctor_id,        
        patient_id=patient_id,
        department=department,
        date=date,
        time=time,
        status     = "PENDING",
    )

    return success_response(message="Appointment booked successfully")

def cancel_slot(request):
    appointment_id = request.data.get("appointment_id")

    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = "CANCELLED"
        appointment.save()
        return success_response(message="Appointment cancelled successfully")
    except Appointment.DoesNotExist:
        return success_response(message="Appointment not found", status=404)

def update_time(request):
    appointment_id = request.data.get("appointment_id")
    new_date      = request.data.get("date")
    new_time      = request.data.get("time")
    patient_id     = request.data.get("patient_id")

    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.date = new_date
        appointment.time = new_time
        appointment.status = "RESCHEDULED"
        appointment.save()
        return success_response(message="Appointment rescheduled successfully")
    except Appointment.DoesNotExist:
        return success_response(message="Appointment not found", status=404)
    



def getAppointment(request):
    role = request.GET.get("role")
    patient_id = request.GET.get("patient_id")
    doctor_id = request.GET.get("doctor_id")

    if role == UserRole.ADMIN:
        return success_response(data=Appointment.objects.all())
    elif role == UserRole.PATIENT and patient_id:
        return success_response(data=Appointment.objects.filter(patient_id=patient_id))
    #  return success_response(message="Unauthorized", status=403)

    #todo
    if role == UserRole.DOCTOR:
        return success_response(data=Appointment.objects.filter(doctor_id=role.user.id))


    return

