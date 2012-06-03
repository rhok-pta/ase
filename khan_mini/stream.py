import time
import cherrypy
from datetime import datetime
import sys, os

OPTIONS = {
    'interval' : {
        'low' : 1,
        'medium' : .5,
        'high' : .3
    },
    'size' : {
        'low' : 10,
        'medium': 40,
        'high' : 90
    },
    'allow_file_cache': False,
    'packet_size' : 90,
    'packet_interval' : 0.3,
    'default_speed' : 'high'
}

class Stream(object):
    
    @cherrypy.expose
    def default(self, topic, video, start=0, bw=OPTIONS['default_speed']):
        """
        This is the method used to server up the flash
        """
        video_filename = '%s/%s/%s' % (cherrypy.server.mediadir, topic, video)
        fi = open(video_filename)

        packet_interval = OPTIONS['interval'][bw]
        packet_size = OPTIONS['size'][bw] * 1042 
        
        file_size = os.path.getsize(video_filename)

        if start > 0:
            file_size = file_size - start + 1
            
        if not OPTIONS['allow_file_cache']:
            #prevent caching...
            cherrypy.response.headers['Expires'] = 'Thu, 19 Nov 1981 08:52:00 GMT'
            cherrypy.response.headers["Last-Modified"] = "%s GMT" % datetime.now().strftime("%a, %b %m %Y %H:%M:%S")
            cherrypy.response.headers["Cache-Control"] = "max-age=0, private, must-revalidate, post-check=0, pre-check=0"
            cherrypy.response.headers["Pragma"] = "no-cache"

        cherrypy.response.headers["Content-Type"] = "video/x-flv"
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="%s"' % video
        cherrypy.response.headers["Content-Length"] = file_size

        fi.seek(start)

        def stream():
            if start != 0:
                yield "FLV\x01\x01\0\0\0\x09\0\0\0\x09"
                    
            data = fi.read(packet_size)
            while len(data) > 0:
                yield data
                data = fi.read(packet_size)

        return stream()
        
    default._cp_config = {'response.stream': True}