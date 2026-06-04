from django.shortcuts import render

from .BaseCtl import Basectl
from ..service.AppointmentService import AppointmentService
from ..service.StudentService import StudentService


class AppointmentListCtl(Basectl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["patient_name"] = requestForm.get("patient_name", "")
        self.form["appointment_date"] = requestForm.get("appointment_date", "")
        self.form["status"] = requestForm.get("status", "")


    def display(self, request, params={}):
        AppointmentListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = AppointmentListCtl.count

        if request.POST['operation'] == "Next":
            AppointmentListCtl.count += 1
            self.form['page_no'] = AppointmentListCtl.count

        if request.POST['operation'] == "Previous":
            AppointmentListCtl.count -= 1
            self.form['page_no'] = AppointmentListCtl.count

        if request.POST['operation'] == "Search":
            AppointmentListCtl.count = 1
            self.form['page_no'] = AppointmentListCtl.count

        self.page_list = self.get_service().search(self.form)

        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res


    def get_template(self):
        return "AppointmentList.html"

    def get_service(self):
        return AppointmentService()

