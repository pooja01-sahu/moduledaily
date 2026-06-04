from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from .ctl.BankNoteCtl import BankNoteCtl
from .ctl.BankNoteListCtl import BankNoteListCtl
from .ctl.BloodBankCtl import BloodBankCtl
from .ctl.BloodBankListCtl import BloodBankListCtl
from .ctl.BranchManagerCtl import BranchManagerCtl
from .ctl.BranchManagerListCtl import BranchManagerListCtl
from .ctl.ChannelCtl import ChannelCtl
from .ctl.ChannelListCtl import ChannelListCtl
from .ctl.BroadCastCtl import BroadCastCtl
from .ctl.BroadCastListCtl import BroadCastListCtl
from .ctl.BatchProcessingCtl import BatchProcessingCtl
from .ctl.LoginCtl import LoginCtl
from .ctl.RegistrationCtl import RegistrationCtl
from .ctl.WelcomeCtl import WelcomeCtl
from .ctl.LogoutCtl import LogoutCtl
from .ctl.StudentCtl import StudentCtl
from .ctl.StudentListCtl import StudentListCtl
from .ctl.MobileCtl import MobileCtl
from .ctl.MobileListCtl import MobileListCtl
from .ctl.AppointmentCtl import AppointmentCtl
from .ctl.AppointmentListCtl import AppointmentListCtl


def info(request, page, action):
    """Log incoming request details (method, page, action, and path) to stdout."""
    print("REQ Method: ", request.method)
    print("Page: ", page)
    print("Action: ", action)
    print("File Path: ", __file__)
    print("Path: ", request.path)
    print("Full Path: ", request.get_full_path)


@csrf_exempt
def action_id(request, page, action="", id=0):
    """Route a request to the controller matching `page`, passing id=0."""
    print("------------------>1")
    info(request, page, action)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {"id": id, "action": action})


@csrf_exempt
def action(request, page, action=""):
    """Route a request to the controller matching `page`, passing id=0."""
    print("------------------>1")
    info(request, page, action)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {"id": 0, "action": action})


@csrf_exempt
def actionId(request, page, id=0):
    """Route a request to the controller matching `page`, passing the given `id`."""
    print("------------------>", id)
    info(request, page, id)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {"id": id})


@csrf_exempt
def auth_action(request, page):
    """Route an authentication request (login, registration, etc.) to the matching controller."""
    print("Auth Action------------------>", page)
    info(request, page, 0)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {})


@csrf_exempt
def preload_router(request, page):
    print('ppppppppppppppppppppppppppppppppppp', page)
    info(request, page, 0)
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    data = ctlObj.preload(request)
    return JsonResponse(data)
