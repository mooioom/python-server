import http.server
import socketserver
import logging
import json
import importlib
import sys
import os
import re

PORT = 80

API_FOLDER          = 'api'
CONTROLLERS_FOLDER  = 'ctrl'
PUBLIC_FOLDER       = 'public'
TEMPLATES_FOLDER    = 'templates'

with open('routes.json') as json_file:
    routes = json.load(json_file)

print( 'Routes', routes )
print( os.getcwd() )

class Handler( http.server.SimpleHTTPRequestHandler ):

    content_types = {
        'html'  : 'text/html',
        'css'   : 'text/css',
        'jpg'   : 'image/jpeg',
        'jpeg'  : 'image/jpeg',
        'js'    : 'text/javascript'
    }

    def respond( self, content = "", content_type = "html" ):

        self.send_response( 200 )
        self.send_header('Content-type', self.content_types[ content_type ] or 'text/html' )
        self.end_headers()
        ba = bytearray()
        ba.extend(map(ord, content))
        self.wfile.write( ba )

    def respondJson( self, data = None ):
        ba = bytearray()
        ba.extend(map(ord,  json.dumps( data ) ))
        self.wfile.write( ba )

    def template( self, template, data = {} ):
        
        f = open( TEMPLATES_FOLDER + '/' + template + '.html' )

        text = f.read()

        for key in data:
            p = re.compile('{{'+key+' ( [^}]* ) }}', re.VERBOSE)
            text = p.sub( str(data[key]), text)

        return text

    def do_POST(self):

        try:

            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            
            data = json.loads( self.data_string )

            uri = str( self.path )

            perfix = '/__api/'

            if( uri.startswith( perfix ) ):

                _api = uri[len(perfix):].split('/')

                module = _api[0]
                method = 'default' if len(_api) == 1 else _api[1]

                if( os.path.isfile( API_FOLDER + '/' + module + '.py' ) ):
                    sys.path.append( API_FOLDER + '/' )
                    api = importlib.import_module( module )
                    getattr( api, method )(*[ self, data ])
                    return

            self.respondJson()

        except IOError:

            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_GET(self):

        try:

            uri = str( self.path )
            file_path = PUBLIC_FOLDER + '/404.html'

            print('GET request,\nURI: ' + uri)

            if( uri.startswith('/__public/') ): 
                file_path = PUBLIC_FOLDER + '/' + uri.split('/__public/')[1]
            else:
                for item in routes:
                    if(item['uri'] == uri): 
                        if 'target' in item.keys() : file_path = PUBLIC_FOLDER + '/' + item['target']
                        if 'controller' in item.keys() :
                            sys.path.append( CONTROLLERS_FOLDER + '/' )
                            ctrl = importlib.import_module( item['controller'] )
                            ctrl.default( self )
                            return

            extension = file_path.split('.')[1]

            f = open( file_path ,'rb')

            self.send_response( 200 )
            self.send_header('Content-type', self.content_types[extension] or 'text/html' )
            self.end_headers()
            self.wfile.write(f.read())

            f.close()

            return

        except IOError:

            self.send_error(404, 'File Not Found: %s' % self.path)

with socketserver.TCPServer(('', PORT), Handler) as httpd:

    print('serving at port', PORT)

    httpd.serve_forever()