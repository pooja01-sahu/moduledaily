from django.shortcuts import render
from .BaseCtl import Basectl
from ..models import Mobile
from ..service.MobileService import MobileService
from ..utility.DataValidator import DataValidator


class MobileCtl(Basectl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["brand_name"] = requestForm.get("brand_name", "")
        self.form["model_name"] = requestForm.get("model_name", "")
        print("model and brand", self.form["brand_name"],self.form["model_name"] )
        self.form["ram"] = requestForm.get("ram", "")
        self.form["price"] = requestForm.get("price" "")

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["brand_name"] = obj.brand_name
        self.form["model_name"] = obj.model_name
        self.form["ram"] = obj.ram
        self.form["price"] = obj.price

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.brand_name = self.form.get("brand_name", "")
        obj.model_name = self.form.get("model_name", "")
        obj.ram = self.form.get("ram", "")
        obj.price = self.form.get("price", "")
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form.get("inputError", {})

        if DataValidator.isNull(self.form.get("brand_name")):
            inputError["brand_name"] = "Brand Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("model_name")):
            inputError["model_name"] = "Model Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("ram")):
            inputError["ram"] = "ram can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("price")):
            inputError["price"] = "price can not be null"
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

        duplicate = self.get_service().get_model().objects.filter(model_name=self.form.get('model_name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Mobile already exist"
        else:
            mobile = self.form_to_model(Mobile())
            print("value in submit",mobile)
            self.get_service().save(mobile)
            self.form['id'] = mobile.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Mobile updated successfully"
            else:
                self.form['message'] = "Mobile added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "AddMobile.html"

    def get_service(self):
        return MobileService()
