from django.db import connection

from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator
from ..models import BranchManager


class BranchManagerService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from scrd_branch where 1=1'
        val = params.get('managerName', None)
        if (DataValidator.isNotNull(val)):
            sql += " and managerName like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize]);
        result = cursor.fetchall()
        columnName = ('id', 'managerName', 'branchName', 'contactNumber')
        res = {
            "data": []
        }
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return BranchManager
