from django.db import connection

from ..models import BatchProcessing
from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator


class BatchProcessingService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from scrd_batchprocessing where 1=1'
        val = params.get('batchCode', None)
        if (DataValidator.isNotNull(val)):
            sql += " and batchCode like" + val + "%%"
        sql += " limit %s %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize]);
        result = cursor.fetchall()
        columnName = ('id', 'batchCode', 'batchName', 'totalRecords', 'status')
        res = {
            "data": []
        }
        params['index'] = (params['pageNo'] - 1) * self.pageSize
        for x in result:
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return BatchProcessing
