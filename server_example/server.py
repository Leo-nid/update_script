from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import logging
import time

import ssl

server_id = 1

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("%s %s", str(self.path), str(time.time()))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        if server_id < 3:
            url = "http://localhost{}".format(self.path)
            nxt_url = "ser{}.local".format(server_id+1)
            r = requests.get(url, headers={'Host':nxt_url})
            

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) < 3:
        raise RuntimeError("not enogh params")
    else:
        server_id = int(argv[2])
        run(port=int(argv[1]))
