from django.db.backends.mysql.validation import DatabaseValidation
from django.shortcuts import render
from django.template.loader import get_template

from ..service.BloodBankService import BloodBankService
from ..utility.DataValidator import DataValidator
from .BaseCtl import Basectl
from ..models import BankNote, BloodBank


class BloodBankCtl(Basectl):

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["bloodGroup"] = obj.bloodGroup
        self.form["unitsAvailable"] = obj.unitsAvailable
        self.form["location"] = obj.location


    def display(self, request, params={}):
        if (params['id'] > 0):
            bank = self.get_service().get(params['id'])
            self.model_to_form(bank)
        return render(request, self.get_template(), {'form': self.form})

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['bloodGroup'] = requestForm['bloodGroup']
        self.form['unitsAvailable'] = requestForm['unitsAvailable']
        self.form['location'] = requestForm['location']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.bloodGroup = self.form['bloodGroup']
        obj.unitsAvailable = self.form['unitsAvailable']
        obj.location = self.form['location']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['bloodGroup'])):
            inputError['bloodGroup'] = "bloodGroup can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['unitsAvailable'])):
            inputError['unitsAvailable'] = "unitsAvailable can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['location'])):
            inputError['location'] = "location can not be null"
            self.form['error'] = True



        return self.form['error']

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(bloodGroup=self.form['bloodGroup'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Bank already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                bank = self.form_to_model(BloodBank())
                self.get_service().save(bank)
                self.form['id'] = bank.id
                self.form['error'] = False
                self.form['message'] = "Bank updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:

            duplicate = self.get_service().get_model().objects.filter(bloodGroup=self.form['bloodGroup'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "BloodBank already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                bank = self.form_to_model(BloodBank())
                self.get_service().save(bank)
                self.form['error'] = False
                self.form['message'] = "BloodBank added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "BloodBank.html"

    def get_service(self):
        return BloodBankService()
