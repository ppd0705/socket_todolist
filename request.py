import json
import urllib


class Request(object):
    def __init__(self, data):
        header, self.body = data.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        request_line = h[0].split()
        self.method = request_line[0]

        path = request_line[1]
        self.parse_path(path)

        self.headers = {}
        self.cookies = {}
        self.add_headers(h[1:])
        self.add_cookies()

    def parse_path(self, path):
        index = path.find('?')
        if index == -1:
            self.path = path
            self.query = {}
        else:
            path, query_string = path.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=', 1)
                query[k] = v
            self.path = path
            self.query = query

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

    def add_headers(self, header):
        for h in header:
            k, v = h.split(': ', 1)
            self.headers[k] = v

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def get_json(self):
        if self.body:
            return json.loads(self.body)

