from django.db.backends.mysql.validation import DatabaseValidation
from django.shortcuts import render
from ..service.BranchManagerService import BranchManagerService
from ..service.ChannelService import ChannelService
from ..utility.DataValidator import DataValidator
from .BaseCtl import Basectl
from ..models import BankNote, BranchManager, Channel


class ChannelCtl(Basectl):

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["channelCode"] = obj.channelCode
        self.form["channelName"] = obj.channelName
        self.form["type"] = obj.type


    def display(self, request, params={}):
        if (params['id'] > 0):
            bank = self.get_service().get(params['id'])
            self.model_to_form(bank)
        return render(request, self.get_template(), {'form': self.form})

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form["channelCode"] = requestForm['channelCode']
        self.form["channelName"] = requestForm['channelName']
        self.form["type"] = requestForm['type']
        self.form["status"] = requestForm['status']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.channelCode = self.form['channelCode']
        obj.channelName = self.form['channelName']
        obj.type = self.form['type']
        obj.status = self.form['status']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['channelCode'])):
            inputError['channelCode'] = "channelCode can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['channelName'])):
            inputError['channelName'] = "channelName can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['type'])):
            inputError['type'] = "type can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['status'])):
            inputError['status'] = "status can not be null"
            self.form['error'] = True


        return self.form['error']

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(channelCode=self.form['channelCode'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Channel already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                branch = self.form_to_model(Channel())
                self.get_service().save(branch)
                self.form['id'] = branch.id
                self.form['error'] = False
                self.form['message'] = "Channel updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:

            duplicate = self.get_service().get_model().objects.filter(channelCode=self.form['channelCode'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Channel already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                branch = self.form_to_model(Channel())
                self.get_service().save(branch)
                self.form['error'] = False
                self.form['message'] = "Channel added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Channel.html"

    def get_service(self):
        return ChannelService()
