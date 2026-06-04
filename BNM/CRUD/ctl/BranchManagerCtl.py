from django.db.backends.mysql.validation import DatabaseValidation
from django.shortcuts import render
from ..service.BranchManagerService import BranchManagerService
from ..utility.DataValidator import DataValidator
from .BaseCtl import Basectl
from ..models import BankNote, BranchManager



class BranchManagerCtl(Basectl):

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["managerName"] = obj.managerName
        self.form["branchName"] = obj.branchName
        self.form["contactNumber"] = obj.contactNumber


    def display(self, request, params={}):
        if (params['id'] > 0):
            bank = self.get_service().get(params['id'])
            self.model_to_form(bank)
        return render(request, self.get_template(), {'form': self.form})

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form["managerName"] = requestForm['managerName']
        self.form["branchName"] = requestForm['branchName']
        self.form["contactNumber"] = requestForm['contactNumber']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.managerName = self.form['managerName']
        obj.branchName = self.form['branchName']
        obj.contactNumber = self.form['contactNumber']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['managerName'])):
            inputError['managerName'] = "managerName can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['branchName'])):
            inputError['branchName'] = "branchName can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['contactNumber'])):
            inputError['contactNumber'] = "contactNumber can not be null"
            self.form['error'] = True


        return self.form['error']

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(managerName=self.form['managerName'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Branch already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                branch = self.form_to_model(BranchManager())
                self.get_service().save(branch)
                self.form['id'] = branch.id
                self.form['error'] = False
                self.form['message'] = "Branch updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:

            duplicate = self.get_service().get_model().objects.filter(managerName=self.form['managerName'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Branch already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                branch = self.form_to_model(BranchManager())
                self.get_service().save(branch)
                self.form['error'] = False
                self.form['message'] = "Branch added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "BranchManager.html"

    def get_service(self):
        return BranchManagerService()
