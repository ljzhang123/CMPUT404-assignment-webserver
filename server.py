#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.data = self.data.split()

        CODE_200 = bytearray("HTTP/1.1 200 OK\r\n", 'utf-8')
        CODE_301 = bytearray("HTTP/1.1 301 Moved Permanently\r\n", 'utf-8')
        CODE_404 = bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8')
        CODE_405 = bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8')
        cssContentType = bytearray("Content-Type: text/css\r\n", 'utf-8')
        htmlContentType = bytearray("Content-Type: text/html\r\n", 'utf-8')

        reqMethod = self.data[0].decode()
        path = self.data[1].decode()

        if reqMethod == 'GET':
            if path.endswith('/'):
                try:
                    with open('www'+path+'index.html', 'r') as file:
                        self.request.sendall(CODE_200 + htmlContentType + bytearray("\r\n" + file.read(), 'utf-8'))
                except FileNotFoundError:
                    self.request.sendall(CODE_404 + bytearray("\r\n", 'utf-8'))
            
            elif path.endswith('.css'):
                try:
                    with open('www'+path, 'r') as file:
                        self.request.sendall(CODE_200 + cssContentType + bytearray("\r\n" + file.read(), 'utf-8'))
                except FileNotFoundError:
                    self.request.sendall(CODE_404 + bytearray("\r\n", 'utf-8'))
            
            elif path.endswith('.html'):
                try:
                    with open('www'+path, 'r') as file:
                        self.request.sendall(CODE_200 + htmlContentType + bytearray("\r\n" + file.read(), 'utf-8'))
                except FileNotFoundError:
                    self.request.sendall(CODE_404 + bytearray("\r\n", 'utf-8'))
            
            elif path.startswith('/../'):
                self.request.sendall(CODE_404 + bytearray("\r\n", 'utf-8'))

            else:
                path += '/'
                try:
                    with open('www'+path+'index.html', 'r') as file:
                        file.read()
                except FileNotFoundError:
                    self.request.sendall(CODE_404 + bytearray("\r\n", 'utf-8'))
                else:
                    self.request.sendall(CODE_301 + bytearray(f"Location: {path}\r\n\r\n", 'utf-8'))

        else:
            self.request.sendall(CODE_405 + bytearray("\r\n", 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()