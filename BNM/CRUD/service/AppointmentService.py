
from django.core.paginator import Paginator

from ..models import Appointment
from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator


class AppointmentService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("patient_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(patient_name__istartswith=value.strip())

        value = params.get("appointment_date", None)
        if DataValidator.isNotNull(value):
            query = query.filter(appointment_date__istartswith=value.strip())

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return Appointment
