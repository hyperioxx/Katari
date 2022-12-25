import asyncio
from Katari import StatefulSIPServer, StatelessSIPServer
from Katari.sip.parser import SIPResponseFactory


app = StatelessSIPServer("udp", "127.0.0.1", 5060)

@app.register_callback("REGISTER")
def register_req(msg):
    return SIPResponseFactory.create_response(status_code=200, reason_phrase="It's OK", headers=msg['headers'])

loop = asyncio.get_event_loop()
loop.run_until_complete(app.run())
