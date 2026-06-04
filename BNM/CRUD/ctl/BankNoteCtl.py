from datetime import datetime

from django.db.backends.mysql.validation import DatabaseValidation
from django.shortcuts import render
from django.template.loader import get_template
from ..utility.DataValidator import DataValidator
from .BaseCtl import Basectl
from ..models import BankNote
from ..service.BankNoteService import BankNoteService


class BankNoteCtl(Basectl):

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["bankName"] = obj.bankName
        self.form["principal"] = obj.principal
        self.form["interestRate"] = obj.interestRate
        self.form["dueDate"] = obj.dueDate


    def display(self, request, params={}):
        if (params['id'] > 0):
            bank = self.get_service().get(params['id'])
            self.model_to_form(bank)
        return render(request, self.get_template(), {'form': self.form})

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['bankName'] = requestForm['bankName']
        self.form['principal'] = requestForm['principal']
        self.form['interestRate'] = requestForm['interestRate']
        self.form['dueDate'] = requestForm['dueDate']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.bankName = self.form['bankName']
        obj.principal = self.form['principal']
        obj.interestRate = self.form['interestRate']
        obj.dueDate = datetime.strptime(self.form['dueDate'],"%Y-%m-%d").date()
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['bankName'])):
            inputError['bankName'] = "BankName can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['principal'])):
            inputError['principal'] = "principal can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['interestRate'])):
            inputError['interestRate'] = "interestRate can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['dueDate'])):
            inputError['dueDate'] = "dueDate can not be null"
            self.form['error'] = True

        return self.form['error']

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(bankName=self.form['bankName'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Bank already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                role = self.form_to_model(BankNote())
                self.get_service().save(role)
                self.model_to_form(role)
                self.form['error'] = False
                self.form['message'] = "Bank updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:

            duplicate = self.get_service().get_model().objects.filter(banName=self.form['bankName'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Bank already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                role = self.form_to_model(BankNote())
                self.get_service().save(role)
                self.form['error'] = False
                self.form['message'] = "Bank added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "BankNote.html"

    def get_service(self):
        return BankNoteService()
