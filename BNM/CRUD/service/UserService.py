
from django.core.paginator import Paginator

from ..models import User
from .BaseService import BaseService
from ..utility.DataValidator import DataValidator

"""
It contains User business logics.   
"""


class UserService(BaseService):

    def authenticate(self, params):
        loginId = params.get("loginId", "").strip()
        password = params.get("password", "").strip()

        query = User.objects.filter(
            loginId=loginId,
            password=password
        )

        print("query =", query)

        if query.exists():
            return query.first()
        else:
            return None

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("firstName", None)
        if DataValidator.isNotNull(value):
            query = query.filter(firstName__istartswith=value.strip())

        value = params.get("lastName", None)
        if DataValidator.isNotNull(value):
            query = query.filter(lastName__istartswith=value.strip())

        value = params.get("loginId", None)
        if DataValidator.isNotNull(value):
            query = query.filter(loginId_istartswith=value.strip())

        value = params.get("gender", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(gender__istartswith=value.strip())

        value = params.get("mobileNumber", None)
        if DataValidator.isNotNull(value):
            query = query.filter(mobileNumber__istartswith=value.strip())


        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return User
