from http.server import BaseHTTPRequestHandler
from download import download_timetable
from parse import parse_timetable
from json import dumps

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = download_timetable()
        timetable = parse_timetable(html)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(dumps(timetable).encode('utf-8'))
        return