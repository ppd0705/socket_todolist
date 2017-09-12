import uuid

from jinja_render import render_template
from models import User, Session
from routes import http_response, redirect, current_user


def register(request):
    if request.method == 'POST':
        form = request.form()
        if User.validate_register(form):
            return redirect('/login')
        else:
            return redirect('/register')
    else:
        body = render_template('register.html')
        return http_response(body)


def login(request):
    if request.method == 'POST':
        form = request.form()
        u = User.validate_login(form)
        if u is not None:
            sid = str(uuid.uuid4())
            kwargs = dict(
                sid=sid,
                user_id=u.id
            )
            Session.new(**kwargs)
            headers = {
                'Set-Cookie': 'sid={}'.format(sid)
            }
            return redirect('/', headers)
    body = render_template('login.html')
    return http_response(body)

def logout(request):
    u =current_user(request)
    Session.delete_one(user_id=u.id)
    headers = {
        'Set-Cookie': 'sid='
    }
    return redirect('/', headers)



def route_dict():
    r = {
        '/register': register,
        '/login': login,
        '/logout': logout,
    }
    return r
