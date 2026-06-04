from django.shortcuts import render

from BNM.CRUD.ctl.BaseCtl import Basectl
from BNM.CRUD.service.BankNoteService import BankNoteService
from BNM.CRUD.utility.DataValidator import DataValidator


class RateLimitCtl(Basectl):

    def submit(self, request, params={}):
        return render(request, self.get_template())

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['rateLimitCode'])):
            inputError['rateLimitcode'] = "rateLimitCode can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['apiName'])):
            inputError['apiName'] = "apiName can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['limitPerMinute'])):
            inputError['limitPerMinute'] = "limitPerMinute can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['status'])):
            inputError['status'] = "status can not be null"
            self.form['error'] = True

    def get_template(self):
        return 'RateLimit.html'

    def get_service(self):
        return BankNoteService()
