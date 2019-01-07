from globals import WEBDIR, res
from http.server import HTTPServer, BaseHTTPRequestHandler
from dig import parse_data
import threading


class HttpProcessor(BaseHTTPRequestHandler):
    def do_POST(self):
        global res
        if self.path == '/wait':
            print("WAITPATH:", self.path)
            content_length = int(self.headers['Content-Length'])
            post_data = (self.rfile.read(content_length)).decode()
            post_data = post_data.split('&')
            print("res check", res)
            if res[0]:
                print("MAKE IT!")
                self.send_response(301)
                self.send_header('Location', '/graph')
                self.end_headers()

        else:
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = (self.rfile.read(content_length)).decode()  # <--- Gets the data itself
            post_data = post_data.split('&')
            t = threading.Thread(target=parse_data, args=(post_data,))
            t.start()
            print("res thread", res)


            #redirect
            self.send_response(301)
            self.send_header('Location', '/wait')
            self.end_headers()



    def do_GET(self):
        paths = {
            '/': {'status': 200, 'header': ('content-type', 'text/html'), 'path': '/index.html'},
            '/graph': {'status': 200, 'header': ('content-type', 'text/html'), 'path': '/graph.html'},
            '/cytoscape.js': {'status': 200, 'header': ('content-type', 'application/javascript'),
                              'path': '/cytoscape.js'},
            '/user_data.js': {'status': 200, 'header': ('content-type', 'application/javascript'),
                              'path': '/user_data.js'},
            '/jquery-3.3.1.min.js': {'status': 200, 'header': ('content-type', 'application/javascript'),
                                     'path': '/jquery-3.3.1.min.js'},
            '/wait': {'status': 200, 'header': ('content-type', 'text/html'), 'path': '/wait_form.html'},
            '404': {'status': 404, 'header': ('content-type', 'text/html'), 'path': '/index.html'},
        }
        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond(paths['404'])

    def handle_http(self, status_code, header, path):
        self.send_response(status_code)
        self.send_header(header[0], header[1])
        self.end_headers()
        return bytes(self.read_static(path))

    def read_static(self, path):
        with open(WEBDIR+path, 'rb') as outfile:
            print(WEBDIR+path)
            content = outfile.read()
        return content

    def respond(self, stat_hd_path):
        response = self.handle_http(stat_hd_path['status'], stat_hd_path['header'], stat_hd_path['path'])
        self.wfile.write(response)


def runserv(server_class=HTTPServer, handler_class=HttpProcessor):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

