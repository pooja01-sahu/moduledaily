from django.core.paginator import Paginator

from ..models import Mobile
from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator


class MobileService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("brand_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(brand_name__istartswith=value.strip())

        value = params.get("model_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(model_name__istartswith=value.strip())

        value = params.get("ram", None)
        if DataValidator.isNotNull(value):
            query = query.filter(ram_istartswith=value.strip())

        value = params.get("price", None)
        if DataValidator.isNotNull(value):
            query = query.filter(price__istartswith=value.strip())


        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return Mobile
