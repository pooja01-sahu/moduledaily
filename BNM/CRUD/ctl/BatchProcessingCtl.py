from django.shortcuts import render

from .BaseCtl import Basectl
from ..service.BatchProcessingService import BatchProcessingService
from ..utility.DataValidator import DataValidator


class BatchProcessingCtl(Basectl):

    def display(self, request, params={}):
        return render(request,self.get_template())
        pass

    def request_to_form(self, requestForm):
        self.form['batchCode'] = requestForm['batchCode']
        self.form['batchName'] = requestForm['batchName']
        self.form['totalRecords'] = requestForm['totalRecords']
        self.form['status'] = requestForm['status']

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNotNull(self.form['batchCode'])):
            inputError['batchError'] = "BatchError can not be null"
            self.form['error'] = True

        if (DataValidator.isNotNull(self.form['batchName'])):
            inputError['batchName'] = "batchName can not be null"
            self.form['error'] = True

        if (DataValidator.isNotNull(self.form['totalRecords'])):
            inputError['totalRecords'] = "BatchError can not be null"
            self.form['error'] = True

        if (DataValidator.isNotNull(self.form['status'])):
            inputError['status'] = "status can not be null"
            self.form['error'] = True

    def submit(self, request, params={}):
        pass

    def get_template(self):
        return 'BatchProcessing.html'

    def get_service(self):
        return BatchProcessingService()




