#!/usr/bin/env python
"""This is a module that consume object desctiptions from
a WebSocket using websocket-client library
(github.com/liris/websocket-client v0.11.0)
Also requires libsvm-3.17
"""

__author__ = "Nicolas, Matias"
__version__ = "0.2"

import argparse
import websocket

from helpers.utils import json
from clasistar import ClassiStar


""" INPUT JSON format (from WebSocket)
{
"_id" : ObjectId("5224a9ca3bdd8c12ea46ee8c"), 
"classified" : -1, 
"clientid" : null, 
"event" : -1, 
"id" : "sdss.2011.53499.509.26", 
"object_path" : "./data/sdss.2011.53499.509.26.json",
"path" : "./images/sdss.2011.53499.509.26.jpg",
"source" : "http://dr10.sdss3.org/...-irg-004649-6-0083.jpg",
"object_data": {"score": 0.032, "fields": ...}
"start_ts": '2013-09-02 21:39:36', 
"end_ts": '2013-09-02 21:39:36',
"creation_ts": '2013-09-02 21:39:36'
"event": 0  0:normal, 1:client, 2:new_client
 }
"""

""" RESPONSE JSON format
{
"id": "sdss.2011.53499.509.26",
"type": 3,  (3 for GALAZY, 6 for STAR)
"sdss_type": 3, (3 for GALAZY, 6 for STAR)
"extra_data": {}
"source": "AUTO",
"level": "AUTO",
"creation_ts: "2013-09-02 21:39:36",
"start_ts": '2013-09-02 21:39:37', 
"end_ts": '2013-09-02 21:39:46',
"event": 100
}

"""

def on_message(ws, message):
    """Callback method on incoming messages

    Receive a incoming message for the classification process.
    When the classification is done, the result is wrapped and
    is written in the WebSocket.

    Args:
        message: String raw message json decodable
    
    Returns:        
        None
    
    Raise:
        Exception: Uncaught exception."""

    j_obj = json.loads(message.strip())

    obj_data = j_obj['object_data']

    cs = ClassiStar(obj_data)

    predicted_type, extra = cs.classify()

    response = {
        "id": j_obj['id'],
        # 3:GALAZY; 6:STAR
        "type": predicted_type,
        "sdss_type": obj_data['objc_type'],
        "extra_data": extra,
        "source": "AUTO",
        "level": "AUTO",
        "clientid": "AUTO",
        "creation_ts": j_obj['creation_ts'],
        "start_ts": j_obj['start_ts'],
        "event": 100
    }

    # Sending response (writing to the websocket)
    ws.write(json.dumps(response))

def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    pass


def run(listen_url):
    # websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        listen_url,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='./ac_hook',
        description='WebSocket Hook for the automatic classifier')

    parser.add_argument(
        '-u', type=str, default='127.0.0.1',
        help='Listening Url (default: 127.0.0.1)')
    parser.add_argument('-p', type=str, default='80',
        help='Listening port (default: 80)')

    args = parser.parse_args()

    url = args.u
    port = args.p

    url_str = "{}:{}/"
    run(url_str.format(url, port))
