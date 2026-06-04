from datetime import datetime

from django.shortcuts import render
from .BaseCtl import Basectl
from ..models import Appointment
from ..service.AppointmentService import AppointmentService
from ..utility.DataValidator import DataValidator


class AppointmentCtl(Basectl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["patient_name"] = requestForm.get("patient_name", "")
        self.form["appointment_date"] = requestForm.get("appointment_date", "")
        self.form["status"] = requestForm.get("status", "")

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["patient_name"] = obj.patient_name
        self.form["appointment_date"] = obj.appointment_date.strftime("%Y-%m-%d") if obj.appointment_date else ""
        self.form["status"] = obj.status

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.patient_name = self.form.get("patient_name", "")
        obj.appointment_date = (
            datetime.strptime(self.form.get("appointment_date"), "%Y-%m-%d").date()
            if self.form.get("appointment_date")
            else None
        )
        obj.status = self.form.get("status", "")
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form.get("inputError", {})

        if DataValidator.isNull(self.form.get("patient_name")):
            inputError["patient_name"] = "Patient Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("appointment_date")):
            inputError["appointment_date"] = "Appointment Date can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("status")):
            inputError["status"] = "Status can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        if params.get("id", 0) > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(patient_name=self.form.get('patient_name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Appointment already exist"
        else:
            appointment = self.form_to_model(Appointment())
            self.get_service().save(appointment)
            self.form['id'] = appointment.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Appointment updated successfully"
            else:
                self.form['message'] = "Appointment added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
        })
        return res

    def get_template(self):
        return "AddAppointment.html"

    def get_service(self):
        return AppointmentService()
