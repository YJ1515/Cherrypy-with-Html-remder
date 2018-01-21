import cherrypy
import json
from mako.template import Template
from utilis import RedisUtiles, Utilies

class Root(object):
    """Root Class."""
    @cherrypy.expose
    def index(self):
        """Method to render index page."""
        redis_utiles = RedisUtiles()
        l=[]
        for top in range(10):
            data = redis_utiles.get_dict('top'+str(top+1))
            l.append(data)
        return Template(filename="index.html").render(list_of_data = l)
    
    @cherrypy.expose
    def search(self, search_name):
        """Method to render search page."""
        redis_utiles = RedisUtiles()
        data = redis_utiles.get_dict(search_name.lower())
        return Template(filename="index.html").render(list_of_data = [data])
    
if __name__ == '__main__':
    utilies = Utilies()
    utilies.read_csv_and_update_redis()
    cherrypy.quickstart(Root(), "/")
