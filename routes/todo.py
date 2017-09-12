from jinja_render import render_template
from routes import (
    http_response,
    login_required,
    current_user)


@login_required
def index(request):
    u = current_user(request)
    body = render_template('todo_index.html', u=u)
    return http_response(body)


def route_dict():
    r = {
        '/todo/index': index,
    }
    return r
