"""This is the server application to receive requests from clients
and loads the astronomics object for manual or automatic classification.
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

import os
import sys
import json
import time
import string
import datetime

import random
from random import choice
from random import shuffle

import pika
from pika.adapters import SelectConnection
import pymongo
from bson.objectid import ObjectId

PORT = 8888


client = pymongo.MongoClient("localhost", 27017)
db = client.test
db.objects.ensure_index([('id', 1)])


class PikaClient(object):

    def __init__(self):
        # Client queue has the class id as name
        self.queue_name = "astrofy-feeder"
    
        # Conncetion values
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None

        # Clients data
        self.client_ids = {}


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
        self.connection = SelectConnection(
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
            auto_delete=False,
            durable=True,
            callback=self.on_exchange_declared
        )


    def on_exchange_declared(self, frame):
        self.channel.queue_declare(
            auto_delete=False,
            queue = self.queue_name,
            durable=True,
            exclusive=False,
            callback=self.on_queue_declared
        )


    def on_queue_declared(self, frame):
        self.channel.queue_bind(
            exchange='astrofy',
            queue=self.queue_name,
            routing_key='astrofy.notify.#',
            callback=None
        )
        self.channel.queue_bind(
            exchange='astrofy',
            queue=self.queue_name,
            routing_key='astrofy.dispatcher.#',
            callback=self.on_queue_bound
        )
    

    def on_queue_bound(self, frame):
        self.channel.basic_consume(
            consumer_callback=self.on_pika_message,
            queue=self.queue_name,
            no_ack=False
        )


    def on_pika_message(self, channel, method, header, body):
        data = json.loads(body)

        # New client notification
        if not data['event']:
            send_to = self.get_client(data['id'])
            if send_to:
                # Normal message
                msg = (" Image source(URL): {0},\n Path: {1},\n "
                       "Object_path: {2},\n Classified: {3}".format(
                            data['source'],
                            data['path'],
                            data['object_path'],
                            data['classified']
                        )
                )
                print msg
                # self.websocket.write_message(
                #     json.dumps(data, sort_keys=True,
                #     indent=4, separators=('<br/>', ': ')))
                self.publish_image(data, 'astrofy.{0}.{1}'.format(
                    send_to, data['classified']))
            else:
                print "***** NO CLIENTS AVALAIBLE *****"

                if not data['classified']:
                    db.objects.update(
                        {"_id": ObjectId(data['_id'])},
                        {"$set": {"classified": 0}})

        else:
            if data['clientid'] != id(self):
                if not self.client_exists(data['clientid']):
                    if data['event'] < 3:
                        self.add_client(data['clientid'])
                elif data['event'] == 3:
                    self.remove_client(data['clientid'])

        print data, ' | ' , id(self)
        print self.client_ids

        self.channel.basic_ack(method.delivery_tag)
        # time.sleep(10)

    def client_exists(self, client_id):
        return client_id in self.client_ids

    def add_client(self, client_id):
        self.client_ids[client_id] = []
        return

    def remove_client(self, client_id):
        if self.client_exists(client_id):
            del self.client_ids[client_id]

    def get_client(self, obj_id):
        if self.client_ids:
            print "*********************************"
            print "*********************************"
            print "*********************************"
            print self.client_ids
            print "*********************************"
            print "*********************************"
            print self.client_ids.keys()
            print "*********************************"
            print "*********************************"
            print "*********************************"
            items = self.client_ids.items()
            shuffle(items)
            for client_id, obj_ids in items:
                if obj_id not in obj_ids:
                    return client_id
        return None

    def on_basic_cancel(self, frame):
        self.connection.close()

    def on_closed(self, connection):
        # self.connection.close()
        self.connection.ioloop.stop()


    def path_generator(self, size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def publish_image(self, obj, rkey):
        properties = pika.BasicProperties(content_type="text/plain",delivery_mode=2)

        data = json.dumps(obj
            # {
            #     "source": "SDSS, DR{0}".format(random.randint(7, 10)),
            #     "path": "/tmp/astrofy/images/{0}.fits".format(self.path_generator()),
            #     "object_data": {
            #         "type": choice(["star", "galaxy", "unknown"]),
            #         "shape": random.randint(1, 20),
            #         "dec": random.randint(0, 360),
            #         "ra": random.randint(0, 90),
            #     },
            #     "classified": 0,
            #     "event": 0,
            #     "clientid": id(self)
            # }
        )

        self.channel.basic_publish(
            exchange='astrofy',
            routing_key=rkey,
            body = data,
            properties=properties
        )


    # def new_client(self, client_id=None):
    #     properties = pika.BasicProperties(content_type="text/plain",delivery_mode=1)

    #     data = json.dumps(
    #         {
    #             "source": None,
    #             "path": "",
    #             "object_data": "",
    #             "classified": 0,
    #             "event": 1,
    #             "clientid": id(self)
    #         }
    #     )
    #     if not client_id:
    #         self.channel.basic_publish(
    #             exchange='astrofy',
    #             routing_key='astrofy.notify',
    #             body = data,
    #             properties=properties
    #         )
    #     else:
    #         self.channel.basic_publish(
    #             exchange='astrofy',
    #             routing_key='astrofy.{0}'.format(client_id),
    #             body = data,
    #             properties=properties
    #         )


    # def remove_client(self, client_id=None):
    #     properties = pika.BasicProperties(content_type="text/plain",delivery_mode=1)

    #     data = json.dumps(
    #         {
    #             "source": None,
    #             "path": "",
    #             "object_data": "",
    #             "classified": 0,
    #             "event": 3,
    #             "clientid": id(self)
    #         }
    #     )

    #     if not client_id:
    #         for cid in self.websocket.client_ids:            
    #             self.channel.basic_publish(
    #                 exchange='astrofy',
    #                 routing_key='astrofy.{0}'.format(cid),
    #                 body = data,
    #                 properties=properties
    #             )
    #     else:
    #         self.channel.basic_publish(
    #             exchange='astrofy',
    #             routing_key='astrofy.{0}'.format(client_id),
    #             body = data,
    #             properties=properties
    #         )


if __name__ == '__main__':

    # # Tornado web application
    # application = TornadoWebServer()

    pc = PikaClient()
    pc.connect()
    pc.connection.ioloop.start()

    # Start the HTTP Server
    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(PORT)

    # # Get a handle to the instance of IOLoop
    # ioloop = tornado.ioloop.IOLoop.instance()

    # # Start the IOLoop
    # ioloop.start()
