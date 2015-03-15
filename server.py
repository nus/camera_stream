# coding: utf-8

import tornado
import tornado.websocket

class NormalRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class StreamHandler(tornado.websocket.WebSocketHandler):
    _clients = []

    def open(self, path):
        if path == u'stream':
            self._clients.append(self)

    def on_message(self, message):
        def w2(c):
            c.write_message(message)
        map(w2, self._clients)

    def on_close(self):
        if self in self._clients:
            self._clients.remove(self)

app = tornado.web.Application([
    (r'/(capturing|stream)', StreamHandler),
    (r'/', NormalRequestHandler),
])

def main():
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
