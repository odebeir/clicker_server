import argparse
import json
import re
from time import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

session_starting_time = time()
session_duration = 20
session_answers = {}
session_choices = []
ip_server = ''

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Just received a GET request")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        s = self.process_request()
        self.wfile.write(s)

        return

    def process_request(self):
        global session_starting_time
        global session_duration
        global session_choices
        global session_answers
        global ip_server

        print self.client_address,' path:',self.path

        s = '<p>your ip is %s</p>'%str(self.client_address[0])

        #if webclient is localhost, admin access is granted
        if str(self.client_address[0]) == ip_server:
            print 'admin access'
            s += '<p>admin access</p>'
            try:
                # starting url is ip/START/A,B,C/14min
                # or ip/START/A,B,C/20sec
                print '*%s*'%self.path[1:]
                k = self.path.split('/')
                print k
                if k[1] == 'START':
                    print 'starting a new session'
                    choices = k[2].split(',')
                    timing = re.split('(\d+)(\w+)',k[3])
                    if timing[2]=='min':
                        session_duration = int(timing[1])*60
                    if timing[2]=='sec':
                        session_duration = int(timing[1])
                    session_choices = choices
                    session_starting_time = time()
                    session_answers = {}
                    print session_choices
                    s += '<p>duration is %f sec</p>'%session_duration
                    s += '<p>choices are in %s</p>'%str(session_choices)

                else:
                    #anonimisation of the answers
                    an_answers = [v for k,v in session_answers.iteritems()]
                    print '*'*80
                    print session_answers
                    print '*'*80
                    s = json.dumps({'choices':session_choices,'answers':an_answers})
            except :
                # problem with admin data
                print 'abort'
                s += '<p>Aborted</p>'
            return s

        else: # simple client access
            print 'client access'
            s += '<form>'
            for c in session_choices:
                s+= '<input type="submit" name="%s" value="%s"><br>' %(c,c)
            s += '</form>'
            print s
            try:
                # check if answer is inside time frame
                delay = time()-session_starting_time
                answer = self.path[1:].lower().split('=')[1]
                if answer in session_choices:
                    if delay < session_duration:
                        #valid answer
                        session_answers[self.client_address[0]] = (answer,delay)
                        s += '<p>delay is %f sec</p>'%delay
                        s += '<p>your answer is %s</p>'%self.path
                    else:
                        s += '<p>sorry, you are %f sec too late</p>'%(delay-session_duration)
                else:
                    s += '<p>sorry %s is not one of the valid answers %s</p>'%(answer,str(session_choices))
                return s
            except :
                return s


    def log_request(self, code=None, size=None):
        print('Request')
        print(code)
        print size
        print self.path

    def log_message(self, format, *args):
        print('Message')

if __name__ == "__main__":
    ip_server = '127.0.0.1'

    parser = argparse.ArgumentParser()
    parser.parse_args()
    try:
        server = HTTPServer(('0.0.0.0', 8000), MyHandler)
        print('Started http server')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()