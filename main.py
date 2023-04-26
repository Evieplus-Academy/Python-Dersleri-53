import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime


class HTMLProcess:
    path = ""

    def process_tags(self, body_data):
        tag_list = re.findall(r'{{(.*)}}', body_data)

        for tag in tag_list:
            match tag:
                case "datetime":
                    body_data = body_data.replace('{{datetime}}', datetime.now().strftime("%a, %d %b %Y %H:%M:%S UTC+03:00"))
                case "path":
                    body_data = body_data.replace('{{path}}', self.path)

        return body_data


class CustomHTTPRequestHandler(BaseHTTPRequestHandler, HTMLProcess):
    def do_GET(self):
        response_code = 404
        body = ""
        match self.path:
            case "/":
                response_code = 200
                with open("index.html") as file_object:
                    body = file_object.read()
                    body = self.process_tags(body)
            case _:
                body = "NOT FOUND"

        self.send_response(response_code)
        self.send_header("Content-type", "text/html")
        self.send_header("Server", "Custom")
        self.end_headers()

        self.wfile.write(body.encode("UTF-8"))


class CustomHTTPServer(HTTPServer):
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

        super().__init__((self.server_ip, self.server_port), CustomHTTPRequestHandler)

    def start(self):
        print(f"Server started at http://{self.server_ip}:{self.server_port}")

        self.serve_forever()


custom_http_server = CustomHTTPServer('localhost', 5000)
custom_http_server.start()