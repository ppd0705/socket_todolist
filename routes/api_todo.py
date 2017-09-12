from models import Todo, User
from routes import json_response


def all(request):
    user_id = request.query.get('id')
    todos = Todo.find_to_json(user_id=user_id)
    return json_response(todos)


def add(request):
    form = request.get_json()
    t = Todo.new(**form)
    return json_response(t.json())



def delete(request):
    id = request.query.get('id')
    Todo.delete_one(id=id)
    return json_response('')


def finish(request):
    id = request.query.get('id')
    form = {
        'id': id,
        'status': '完成'
    }
    Todo.update_one(**form)
    return json_response('')


def route_dict():
    d = {
        '/api/todo/all': all,
        '/api/todo/add': add,
        '/api/todo/delete': delete,
        '/api/todo/finish': finish,
    }
    return d
