from django.db.backends.mysql.validation import DatabaseValidation
from django.shortcuts import render
from django.template.loader import get_template
from ..service.BroadCastService import BroadCastService
from ..utility.DataValidator import DataValidator
from .BaseCtl import Basectl
from ..models import Broadcast


class BroadCastCtl(Basectl):

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["broadcastCode"] = obj.broadcastCode
        self.form["broadMessage"] = obj.broadMessage
        self.form["sentBy"] = obj.sentBy
        self.form["status"] = obj.status


    def display(self, request, params={}):
        if (params['id'] > 0):
            bank = self.get_service().get(params['id'])
            self.model_to_form(bank)
        return render(request, self.get_template(), {'form': self.form})

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['broadcastCode'] = requestForm['broadcastCode']
        self.form['broadMessage'] = requestForm['broadMessage']
        self.form['sentBy'] = requestForm['sentBy']
        self.form['status'] = requestForm['status']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.broadcastCode = self.form['broadcastCode']
        obj.broadMessage = self.form['broadMessage']
        obj.sentBy = self.form['sentBy']
        obj.status = self.form['status']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['broadcastCode'])):
            inputError['broadcastCode'] = "broadcastCode can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['broadMessage'])):
            inputError['broadMessage'] = "broadMessage can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['sentBy'])):
            inputError['sentBy'] = "sentBy can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['status'])):
            inputError['status'] = "status can not be null"
            self.form['error'] = True



        return self.form['error']

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(broadcastCode=self.form['broadcastCode'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Bank already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                bank = self.form_to_model(Broadcast())
                self.get_service().save(bank)
                self.form['id'] = bank.id
                self.form['error'] = False
                self.form['message'] = "Bank updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:

            duplicate = self.get_service().get_model().objects.filter(broadcastCode=self.form['broadcastCode'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "BloodBank already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                bank = self.form_to_model(Broadcast())
                self.get_service().save(bank)
                self.form['error'] = False
                self.form['message'] = "BloodBank added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "BroadCast.html"

    def get_service(self):
        return BroadCastService()
