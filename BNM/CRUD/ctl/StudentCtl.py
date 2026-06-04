from datetime import datetime

from django.shortcuts import render

from .BaseCtl import Basectl
from ..models import StudentManagment
from ..service.StudentService import StudentService
from ..utility.DataValidator import DataValidator


class StudentCtl(Basectl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["first_name"] = requestForm.get("first_name","")
        self.form["last_name"] = requestForm.get("last_name","")
        self.form["dob"] = requestForm.get("dob","")
        self.form["email"] = requestForm.get("email" "")
        self.form["mobile_no"] = requestForm.get("mobile_no","")
        self.form["course"] = requestForm.get("course","")

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["first_name"] = obj.first_name
        self.form["last_name"] = obj.last_name
        self.form["email"] = obj.email
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["mobile_no"] = obj.mobile_no
        self.form["course"] = obj.course

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.first_name = self.form.get("first_name", "")
        obj.last_name = self.form.get("last_name", "")
        obj.email = self.form.get("email", "")
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.mobile_no = self.form.get("mobile_no", "")
        obj.course = self.form.get("course", "")
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form.get("inputError", {})

        if DataValidator.isNull(self.form.get("first_name")):
            inputError["first_name"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("last_name")):
            inputError["last_name"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("dob")):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("email")):
            inputError["email"] = "Login can not be null"
            self.form["error"] = True
        elif not DataValidator.isemail(self.form.get("email")):
            inputError["email"] = "Login must be a valid email address"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobile_no")):
            inputError["mobile_no"] = "Mobile Number can not be null"
            self.form["error"] = True
        elif not DataValidator.isMobileNumber(self.form.get("mobile_no")):
            inputError["mobile_no"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("course")):
            inputError["course"] = "Course can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        if params.get("id", 0) > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        print("here submit calllllllll")

        pk = int(self.form.get('id', 0))
        print("here check pk",pk)

        duplicate = self.get_service().get_model().objects.filter(email=self.form.get('email', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Student already exist"
        else:
            student = self.form_to_model(StudentManagment())
            self.get_service().save(student)
            self.form['id'] = student.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Student updated successfully"
            else:
                self.form['message'] = "Student added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "AddStudent.html"

    def get_service(self):
        return StudentService()





