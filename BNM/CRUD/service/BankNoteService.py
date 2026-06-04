from django.db import connection

from .BaseService import BaseService
from ..models import BankNote
from ..utility.DataValidator import DataValidator


class BankNoteService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from scrd_banknote where 1=1'
        val = params.get('bankName', None)
        if (DataValidator.isNotNull(val)):
            sql += " and bankName like '" + val + "%%'"
        duedate = params.get('dueDate', None)
        if (DataValidator.isNotNull(duedate)):
            sql += " and dueDate='" + duedate + "'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize]);
        result = cursor.fetchall()
        columnName = ('id', 'bankName', 'principal', 'interestRate', 'dueDate')
        res = {
            "data": []
        }
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return BankNote
