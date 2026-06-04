from django.core.paginator import Paginator

from ..models import StudentManagment
from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator


class StudentService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("first_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(first_name__istartswith=value.strip())

        value = params.get("last_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(last_name__istartswith=value.strip())

        value = params.get("email", None)
        if DataValidator.isNotNull(value):
            query = query.filter(email_istartswith=value.strip())

        value = params.get("mobile_no", None)
        if DataValidator.isNotNull(value):
            query = query.filter(mobile_no__istartswith=value.strip())

        value = params.get("course", None)
        if DataValidator.isNotNull(value):
            query = query.filter(course__istartswith=value.strip())

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return StudentManagment
