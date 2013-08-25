"""This is the server application to receive requests from clients
and loads the astronomics object for manual or automatic classification.
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

import os
import sys
import json
import datetime

from random import choice

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import options, define

import pika
from pika.adapters.tornado_connection import TornadoConnection

# Define available options
define("port", default=8888, type=int, help="run on the given port")
define("cookie_secret", help="random cookie secret")
define("queue_host", default="127.0.0.1", help="Host for amqp daemon")
define("queue_user", default="guest", help="User for amqp daemon")
define("queue_password", default="guest", help="Password for amqp daemon")

PORT = 8888


class PikaClient(object):

    def __init__(self):
        # Client queue has the class id as name
        self.queue_name = "astrofy_client-{0}".format(id(self))
    
        # Conncetion values
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None

        # Websocket object
        self.websocket = None


    def connect(self):
        if self.connecting:
            return
        
        self.connecting = True

        # Connecting to RabbitMQ using default values
        credentials = pika.PlainCredentials('guest', 'guest')
        param = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            virtual_host="/",
            credentials=credentials
        )
        self.connection = TornadoConnection(
            param,
            on_open_callback=self.on_connected
        )


    def on_connected(self, connection):
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)


    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.exchange_declare(
            exchange='astrofy',
            type='topic',
            auto_delete=True,
            durable=False,
            callback=self.on_exchange_declared
        )


    def on_exchange_declared(self, frame):
        self.channel.queue_declare(
            auto_delete=True,
            queue = self.queue_name,
            durable=False,
            exclusive=True,
            callback=self.on_queue_declared
        )


    def on_queue_declared(self, frame):
        self.channel.queue_bind(
            exchange='astrofy',
            queue=self.queue_name,
            routing_key='astrofy.notify.#'.format(id(self)),
            callback=None
        )
        self.channel.queue_bind(
            exchange='astrofy',
            queue=self.queue_name,
            routing_key='astrofy.{0}.#'.format(id(self)),
            callback=self.on_queue_bound
        )
    

    def on_queue_bound(self, frame):
        self.new_client()
        self.channel.basic_consume(
            consumer_callback=self.on_pika_message,
            queue=self.queue_name,
            no_ack=True
        )


    def on_pika_message(self, channel, method, header, body):
        data = json.loads(body)

        # New client notification
        if 'new_client' in data:
            if data['id'] != id(self):
                if not self.websocket.client_exists(data['id']):
                    self.websocket.add_client(data['id'])
                if data['new_client']:
                    self.new_client(False, data['id'])
        else:
            msg = "{0} says({1}): {2}".format(
                data['id'],
                str(datetime.datetime.now()),
                data['msg']
            )
            self.websocket.write_message(msg)

        print data, ' | ' , id(self)
        print self.websocket.client_ids


    def on_basic_cancel(self, frame):
        self.websocket.remove_client(id(self))
        self.connection.close()


    def on_closed(self, connection):
        tornado.ioloop.IOLoop.instance().stop()


    def sample_message(self, ws_msg):
        properties = pika.BasicProperties(content_type="text/plain",delivery_mode=1)

        data = json.dumps({"msg": ws_msg, "id": id(self)})
        self.channel.basic_publish(
            exchange='astrofy',
            routing_key='astrofy.{0}'.format(
                choice(self.websocket.client_ids)),
            body = data,
            properties=properties
        )


    def new_client(self, new=True, client_id=None):
        properties = pika.BasicProperties(content_type="text/plain",delivery_mode=1)

        data = json.dumps({"new_client": new, "id": id(self)})
        if not client_id:
            self.channel.basic_publish(
                exchange='astrofy',
                routing_key='astrofy.notify',
                body = data,
                properties=properties
            )
        else:
            self.channel.basic_publish(
                exchange='astrofy',
                routing_key='astrofy.{0}'.format(client_id),
                body = data,
                properties=properties
            )


class LiveChat(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):

        self.render(
            "astrofy.html",
            connected=self.application.pika.connected
        )


class WebSocketServer(tornado.websocket.WebSocketHandler):
    'WebSocket Handler, Which handle new websocket connection.'

    def open(self):
        'Websocket Connection opened.'
        self.client_ids = []
        self.pika_client = PikaClient()
        self.pika_client.websocket = self

        ioloop.add_timeout(1000, self.pika_client.connect)

    def on_message(self,msg):
        'A message on the Webscoket.'

        print "Message: [{0}] on the Websocket".format(msg)
        self.pika_client.sample_message(msg)

    def on_close(self):
        'Closing the websocket ...'

        print "WebSocket Closed"        
        self.pika_client.connection.close()

    def client_exists(self, client_id):
        return client_id in self.client_ids

    def add_client(self, client_id):
        self.client_ids.append(client_id)

    def remove_client(self, client_id):
        try:
            self.client_ids.remove(client_id)
        except ValueError:
            return


class TornadoWebServer(tornado.web.Application):

    def __init__(self):

        # Urls for mapping requests
        handlers = [

                (r"/ws_channel",WebSocketServer),
                (r"/astrofy",LiveChat)
        ]

        # Other basics settings
        settings = dict(
            cookie_secret = options.cookie_secret,
            login_url = "/signin",
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookies = True,
            debug = True
        )

        # Initialize base class
        tornado.web.Application.__init__(self,handlers,**settings)


if __name__ == '__main__':

    # Tornado web application
    application = TornadoWebServer()

    pc = PikaClient()
    application.pika = pc

    # Start the HTTP Server
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)

    # Get a handle to the instance of IOLoop
    ioloop = tornado.ioloop.IOLoop.instance()

    # Start the IOLoop
    ioloop.start()
