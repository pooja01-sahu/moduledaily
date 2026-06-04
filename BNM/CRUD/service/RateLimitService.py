from django.db import connection

from .BaseService import BaseService
from ..utility.DataValidator import DataValidator
from ..models import RateLimit


class RateLimitService(BaseService):

    def search(self,params):
        pageNo = (params['pageNo']- 1) * self.pageSize
        sql = 'select * from scrd_ratelimit where 1=1'
        val = params.get('rateLimitCode',None)
        if (DataValidator.isNotNull(val)):
            sql += " And rateLimitCode like" + val + "%%"
        sql += ' limit %s, %s'
        cursor = connection.cursor()
        cursor.execute(sql,[pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id',"rateLimitCode",'apiName','limitPerMinute','status')
        res = {'data':[]}
        params['index'] =((params['pageNo']-1) * self.pageSize)
        for x in result:
              params['maxId'] = x[0]
              res['data'].append({columnName[i]: x[i] for i,_ in enumerate(x)})
        return res

    def get_model(self):
        return RateLimit