from .BaseCtl import Basectl
from django.shortcuts import redirect


class LogoutCtl(Basectl):

    def display(self, request, _params={}):
        request.session.flush()
        return redirect('/Login/')

    def submit(self, request, _params={}):
        request.session.flush()
        return redirect('/Login/')

    def get_template(self):
        return "Login.html"

    def get_service(self):
        pass
