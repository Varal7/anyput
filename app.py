from tornado import websocket, web, ioloop
import json

cl = []


def update_clients():
    broadcast(json.dumps({
        'type': 'nb_clients',
        'value': len(cl)
    }))

def broadcast(message):
    for c in cl:
        c.write_message(message)

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)
        update_clients()

    def on_close(self):
        if self in cl:
            cl.remove(self)
        update_clients()

    def update_progress(self, percentage):
        progress_message = json.dumps({
            'type': 'progress_update',
            'value': percentage
        })
        self.write_message(progress_message)

class ApiHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        pass

    @web.asynchronous
    def post(self):
        value = self.get_argument("value")
        key = self.get_argument("key")
        with open("keys.txt") as f:
            keys = [k.strip() for k in f.readlines()]
        if key in keys:
            message = json.dumps({
                'type': 'output',
                'value': value,
            })
            broadcast(message)
            self.write('Sent')
            self.finish()
        else:
            print(key)
            print(keys)
            self.write('Not allowed')
            self.finish()

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/api', ApiHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(search.js|style.css|img/giphy.gif)', web.StaticFileHandler, {'path': './'}),
], debug=True)

if __name__ == '__main__':
    app.listen(8889)
    ioloop.IOLoop.instance().start()
