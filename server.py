import http.server
import socketserver
import logging
import json
import importlib
import smtplib
import sys
import os
import re

import urllib.parse as urlparse
from urllib.parse import parse_qs

PORT = 80
if(1 in range(len(sys.argv))): PORT = sys.argv[1]

API_FOLDER         = 'api'
CONTROLLERS_FOLDER = 'ctrl'
PUBLIC_FOLDER      = 'public'
TEMPLATES_FOLDER   = 'templates'

API_PREFIX    = '/__api/'
PUBLIC_PREFIX = '/__public/'

#emailer

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

SMTP_USER     = ''
SMTP_PASSWORD = ''

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

    def respondFile( self, file_path ):

        try:
            extension = file_path.split('.')[1]
        except:
            extension = 'html'

        f = open( file_path ,'rb')

        self.send_response( 200 )
        self.send_header('Content-type', self.content_types[extension] or 'text/html' )
        self.end_headers()
        self.wfile.write(f.read())

        f.close()

    def template( self, template, data = {} ):
        
        f = open( TEMPLATES_FOLDER + '/' + template + '.html' )

        text = f.read()

        for key in data:
            p = re.compile('{{'+key+' ( [^}]* ) }}', re.VERBOSE)
            text = p.sub( str(data[key]), text)

        return text

    def api_handler( self ):

        uri = str( self.path )

        if( uri.startswith( API_PREFIX ) ):

            try:
                self.post_data_string = self.rfile.read(int(self.headers['Content-Length']))
                postData = json.loads( self.post_data_string )
            except:
                postData = {}

            parsed  = urlparse.urlparse(uri)
            getData = parse_qs(parsed.query)

            _api = uri[len(API_PREFIX):].split('/')

            module = _api[0]
            method = 'default' if len(_api) == 1 else _api[1]

            if( os.path.isfile( API_FOLDER + '/' + module + '.py' ) ):
                sys.path.append( API_FOLDER + '/' )
                api = importlib.import_module( module )
                getattr( api, method )(*[ self, postData, getData ])
                return True
        
        return False

    def email(self, to = [], subject = '', body = '' ):

        user     = SMTP_USER
        password = SMTP_PASSWORD

        sent_from = user

        email = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL( SMTP_HOST , SMTP_PORT )
            server.ehlo()
            server.login( user, password )
            server.sendmail( sent_from, to, email )
            server.close()

            print('Email sent!')

        except Exception as e:

            print('Email error :: ' + str(e) )

    def do_POST(self):

        try:

            if( self.api_handler() ): return

            self.respondJson()

        except IOError:

            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_GET(self):

        try:

            uri = str( self.path )

            print('GET request,\nURI: ' + uri)

            if( self.api_handler() ): return

            file_path = PUBLIC_FOLDER + '/' + uri

            if( uri == '/' ): file_path = PUBLIC_FOLDER + '/' + 'index.html'
            
            for item in routes:
                if(item['uri'] == uri): 
                    if 'target' in item.keys() : file_path = PUBLIC_FOLDER + '/' + item['target']
                    if 'controller' in item.keys() :
                        sys.path.append( CONTROLLERS_FOLDER + '/' )
                        ctrl = importlib.import_module( item['controller'] )
                        ctrl.default( self )
                        return

            self.respondFile( file_path )            

            return

        except IOError:

            self.respondFile( PUBLIC_FOLDER + '/404.html' )

with socketserver.TCPServer(('', PORT), Handler) as httpd:

    print('serving at port', PORT)

    httpd.serve_forever()