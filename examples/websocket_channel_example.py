import websocket
try:
    import thread
except ImportError:  # TODO use Threading instead of _thread in python3
    import _thread as thread
import time
import sys
import ssl

def on_message(ws, message):
    print('on_message: {}'.format(message))


def on_error(ws, error):
    print('on_error: {}'.format(error))


def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "wss://dev.dstcontrols.com/piwebapi/streams/P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/channel"
    else:
        host = sys.argv[1]
    
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header={'Authorization':'Basic YWstcGl3ZWJhcGktc3ZjOkRQJDI4R2hNeXAqIUUmZ2M='})
                                
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    print('does this get hit?') #answer: no