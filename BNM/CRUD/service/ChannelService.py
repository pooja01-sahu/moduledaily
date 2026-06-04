from django.db import connection

from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator
from ..models import Channel


class ChannelService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from scrd_channel where 1=1'
        val = params.get('channelCode', None)
        if (DataValidator.isNotNull(val)):
            sql += " and channelCode like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize]);
        result = cursor.fetchall()
        columnName = ('id', 'channelCode', 'channelName', 'type',"status")
        res = {
            "data": []
        }
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Channel
