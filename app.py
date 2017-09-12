import socket
import _thread

from request import Request
from routes import error
from routes.api_todo import route_dict as api_todo
from routes.index import route_dict as route_index
from routes.todo import route_dict as route_todo
from routes.user import route_dict as roure_user


def response_for_path(request):
    routes = {}
    routes.update(api_todo())
    routes.update(route_index())
    routes.update(route_todo())
    routes.update(roure_user())
    response = routes.get(request.path, error)
    return response(request)


def process_request(conn):
    r = conn.recv(1024)
    r = r.decode()
    parts = r.split()
    if len(parts) > 0:
        request = Request(r)
        print('<request>::: ', r)
        response = response_for_path(request)
        if 'static' not in request.path and response is not None:
            print('<response:::>', response.decode())
        conn.sendall(response)
    conn.close()


def run(host, port):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        print('开始监听 {}：{}'.format(host, port))
        while True:
            conn, addr = s.accept()
            # _thread.start_new_thread(process_request, (conn,))

            # 单线程
            process_request(conn)


if __name__ == '__main__':
    config = dict(
        host='127.0.0.1',
        port=2333
    )
    run(**config)
