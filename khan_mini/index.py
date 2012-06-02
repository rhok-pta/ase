import cherrypy
import urllib2
import json

# Jinja templating engine
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

KHAN_BASE_URL = "http://localhost:8080/"

class KhanAcademyMini(object):

    @cherrypy.expose    
    def index(self, topic='root'):
        url = "http://localhost:8080/api/v1/topic/%s" % topic
        response = urllib2.urlopen(url).read()
        data = json.loads(response)
        tmpl = env.get_template('index.html')
        return tmpl.render(data)
        
    @cherrypy.expose    
    def video(self, vid_id='root'):
        url = "http://localhost:8080/api/v1/videos/%s" % vid_id
        response = urllib2.urlopen(url).read()
        data = json.loads(response)
        tmpl = env.get_template('video.html')
        return tmpl.render(data)

    @cherrypy.expose    
    def exercise(self, exercise_id='root'):
        url = "http://localhost:8080/api/v1/exercises/%s" % exercise_id
        response = urllib2.urlopen(url).read()
        data = json.loads(response)
        data['khan_base_url'] = KHAN_BASE_URL
        tmpl = env.get_template('exercise.html')
        return tmpl.render(data)


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                         'server.socket_port': 8081,
                        }) 

cherrypy.quickstart(KhanAcademyMini())