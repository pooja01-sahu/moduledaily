from django.shortcuts import render

from .BaseCtl import Basectl
from ..service.MobileService import MobileService
from ..service.StudentService import StudentService


class MobileListCtl(Basectl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["brand_name"] = requestForm.get("brand_name", "")
        self.form["model_name"] = requestForm.get("model_name", "")
        self.form["ram"] = requestForm.get("ram", "")
        self.form["price"] = requestForm.get("price" "")

    def display(self, request, params={}):
        MobileListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = MobileListCtl.count

        if request.POST['operation'] == "Next":
            MobileListCtl.count += 1
            self.form['page_no'] = MobileListCtl.count

        if request.POST['operation'] == "Previous":
            MobileListCtl.count -= 1
            self.form['page_no'] = MobileListCtl.count

        if request.POST['operation'] == "Search":
            MobileListCtl.count = 1
            self.form['page_no'] = MobileListCtl.count

        self.page_list = self.get_service().search(self.form)

        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res


    def get_template(self):
        return "MobileList.html"

    def get_service(self):
        return MobileService()

