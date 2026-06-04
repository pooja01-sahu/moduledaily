from django.shortcuts import render

from .BaseCtl import Basectl
from ..service.StudentService import StudentService


class StudentListCtl(Basectl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["first_name"] = requestForm.get("first_name", "")
        self.form["last_name"] = requestForm.get("last_name", "")
        self.form["dob"] = requestForm.get("dob", "")
        self.form["email"] = requestForm.get("email" "")
        self.form["mobile_no"] = requestForm.get("mobile_no", "")
        self.form["course"] = requestForm.get("course", "")

    def display(self, request, params={}):
        StudentListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = StudentListCtl.count

        if request.POST['operation'] == "Next":
            StudentListCtl.count += 1
            self.form['page_no'] = StudentListCtl.count

        if request.POST['operation'] == "Previous":
            StudentListCtl.count -= 1
            self.form['page_no'] = StudentListCtl.count

        if request.POST['operation'] == "Search":
            StudentListCtl.count = 1
            self.form['page_no'] = StudentListCtl.count

        self.page_list = self.get_service().search(self.form)

        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res


    def get_template(self):
        return "StudentList.html"

    def get_service(self):
        return StudentService()

