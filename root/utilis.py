import zipfile
import pandas as pd
import redis

redis_ins = redis.Redis('localhost')

class Utilies:
    """Utilies class."""
    def read_csv_and_update_redis(self):
        "Metod to read csv from zip and upload data to Redis."
        f = zipfile.ZipFile('../EQ190118_CSV.ZIP')
        df= pd.read_csv(f.open('EQ190118.CSV'))
        df1 = df.filter(['SC_CODE', 'SC_NAME', 'OPEN',	'HIGH',	'LOW','CLOSE'], axis=1)
        
        redis_utiles = RedisUtiles()
        
        #All Stocks to redis
        list_of_df = df1.to_dict('records')
        for data in list_of_df:
            redis_utiles.set_dict(data.get('SC_NAME').lower().strip(), data)
            
        #Top 10 Stocks to redis
        sorted_df = df1.sort_values('HIGH', ascending=False).head(10)
        list_of_df = sorted_df.to_dict('records')
        top = 0
        for data in list_of_df:
            top = top +1
            redis_utiles.set_dict(('TOP'+str(top)).lower(),data)


class RedisUtiles:
    """RedisUtiles Class."""
        
    def set_dict(self, key, value):
        """Set dict value to redis."""
        redis_ins.hmset(key, value)
        
    def get_dict(self, key):
        """Get dict value to redis."""
        value = redis_ins.hgetall(key)
        return value
        
    def get_all_dict(self):
        """Get dict value to redis."""
        keys = redis_ins.keys()
        l =[]
        for key in keys:
            value = redis_ins.hgetall(key)
            l.append(value)
