from django.db import connection

from .BaseService import BaseService
from ..models import BloodBank
from ..utility.DataValidator import DataValidator


class BloodBankService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from scrd_bankblood where 1=1'
        val = params.get('bloodGroup', None)
        if (DataValidator.isNotNull(val)):
            sql += " and bloodGroup like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize]);
        result = cursor.fetchall()
        columnName = ('id', 'bloodGroup', 'unitsAvailable', 'location')
        res = {
            "data": []
        }
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return BloodBank
