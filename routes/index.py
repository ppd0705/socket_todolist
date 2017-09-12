from jinja_render import render_template
from routes import current_user, login_required
from routes import http_response

@login_required
def index(request):
    u = current_user(request)
    body = render_template('index.html', username=u.username)
    return http_response(body)

@login_required
def static(request):
    print('233333333')
    filename = request.query.get('file','')
    print('file', filename)
    path = 'static/' + filename
    print('statis path', path)
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        response = header + f.read()
        return response

def route_dict():
    r = {
        '/': index,
        '/static': static,
    }
    return r
