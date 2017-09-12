import json

from models import (
    Session,
    User,
)


def current_user(request):
    sid = request.cookies.get('sid', '')
    print('current sid', sid)
    s = Session.find_one(sid=sid)
    print('get session', s)
    if s is not None:
        u = User.find_one(id=s.user_id)
        print('get user', u)
        return u
    else:
        return None


def response_with_headers(headers=None, status_code=200):
    header = 'HTTP/1.1 {} XX\r\nContent-Type: text/html\r\n'.format(status_code)
    if headers is not None:
        header += ''.join([
            '{}: {}\r\n'.format(k, v) for k, v in headers.items()
        ])
    return header


def redirect(location, headers=None):
    h = {'location': location}
    if headers is not None:
        h.update(headers)
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode()


def login_required(func):
    def f(request):
        u = current_user(request)
        if u is None:
            return redirect('/login')
        else:
            return func(request)
    return f


def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>SORRY! NOT FOUND</h1>'
    }
    return e.get(code, b'')


def http_response(body, headers=None):
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data):
    header = 'HTTP/1.1 200 OK\r\n'
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode()
