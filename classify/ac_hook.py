"""This is a module that consume object desctiptions from
a WebSocket using websocket-client library
(github.com/liris/websocket-client v0.11.0)
Also requires libsvm-3.17
"""

__author__ = "Nicolas, Matias"
__version__ = "0.1"

import websocket # v0.11.0
import thread
import time

try:
    import simplejson as json
except ImportError:
    import json
    # Avoid SumblimeLinter warnings
    json

example = {"userid": 12345, "uri": "www.pics.com/Gf21c0"}
msg = json.dumps(example)


def on_message(ws, message):
    try:
        j_obj = json.loads(message.strip())
        print j_obj["userid"]

        # TODO: Fetch the files
        # TODO: Classify the object

    except Exception:
        print message


def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    def ask(*args):
        ws.send(msg)
        while True:
            response = raw_input("Send a message (exit to quit): ")
            if response == 'exit':
                time.sleep(1)
                break
            ws.send(response)
            time.sleep(1)
        print "thread terminating..."
        ws.close()

    thread.start_new_thread(ask, ())


def run(*args):
    # websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        "ws://echo.websocket.org/",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    run()
