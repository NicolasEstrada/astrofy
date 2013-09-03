"""This is the server application to receive requests from clients
and loads the astronomics object for manual or automatic classification.
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

import os
import sys
import json
import string
import datetime

import random
from random import choice


import pymongo
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
from tornado.options import options, define

import pika
from pika.adapters import SelectConnection

from helpers.utils import logger
from helpers.utils import wait

# SDSS3 query to get ids
# http://api.sdss3.org/spectrumQuery?&limit=5&urls&ra=159.815d&dec=-0.655&radius=900
# SDSS3 query to get a JSON 
# http://api.sdss3.org/spectrum?id=sdss.274.51913.92.26&format=json

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
            auto_delete=True,
            durable=False,
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
            routing_key='astrofy.dispatcher.#',
            callback=self.on_queue_bound
        )
    

    # def on_queue_bound(self, frame):

    #     # self.connection.ioloop.stop()



    def on_basic_cancel(self, frame):
        self.connection.close()

    def on_closed(self, connection):
        # self.connection.close()
        self.connection.ioloop.stop()


    def publish_image(self, astfy_obj):
        properties = pika.BasicProperties(content_type="text/plain",delivery_mode=2)

        data = json.dumps(astfy_obj
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
            #     "client_id": id(self)
            # }
        )

        self.channel.basic_publish(
            exchange='astrofy',
            routing_key='astrofy.dispatcher',
            body = data,
            properties=properties
        )


    def on_queue_bound(self, unused_frame):
        print "Queue bound"
        print "Start ..."
        while True:
            while(db.objects.find({"classified": 0}).count() > 0):
                print "getting objects ..."
                obj = db.objects.find_one({"classified": 0})
                print obj['id']
                obj_id = obj['_id']
                obj['_id'] = str(obj['_id'])
                self.publish_image(obj)
                db.objects.update({"_id": obj_id}, {"$set": {"classified": -1}})

                wait(logger, 10, False)
            wait(logger, 600, False)


if __name__ == '__main__':

    # Tornado web application
    # application = TornadoWebServer()

    # try:
    pc = PikaClient()
    pc.connect()
    pc.connection.ioloop.start()

    # print "Start ..."
    # while(db.objects.find({"classified": 0}).count() > 0):
    #     print "getting objects ..."
    #     obj = db.objects.find_one({"classified": 0})
    #     print obj
    #     obj['_id'] = str(obj['_id'])
    #     pc.publish_image(obj)

    #     wait(logger, 10, False)
    # except Exception, e:
    #     print e
    #     pc.connection.ioloop.stop()
    #     raise Exception

    # Start the HTTP Server
    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(PORT)

    # Get a handle to the instance of IOLoop
    # ioloop = tornado.ioloop.IOLoop.instance()

    # Start the IOLoop
    # ioloop.start()