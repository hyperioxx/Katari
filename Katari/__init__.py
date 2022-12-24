from Katari.sockets import create_socket, AsyncTCPSocket, WebSocket, AsyncUDPSocket
from Katari.sip import SIPParser, SIPStatusCodeError, SIPResponseFactory

class SIPServer:
    def __init__(self, socket_type, host, port):
        self.host = host
        self.port = port
        self.socket = create_socket(socket_type, host, port)
        self.callbacks = {}

    def register_callback(self, method, callback):
        """
        Register a callback function for a SIP method.

        :param method: The SIP method to register the callback for.
        :type method: str
        :param callback: The callback function to register.
        :type callback: function
        """
        try:
            self.callbacks[method] = callback
        except KeyError:
            raise SIPStatusCodeError(status_code=501, reason_phrase="Not Implemented")

    def get_callback(self, method):
        try:
            return self.callbacks[method] 
        except KeyError:
            raise SIPStatusCodeError(status_code=501, reason_phrase="Not Implemented")


    async def run(self):
        if isinstance(self.socket, AsyncUDPSocket):
            # Store the address of the client that sent the data
            while True:
                data, address = await self.socket.receive()
                parsed_message = SIPParser().parse(data)
                try:
                    # Call the callback function for the SIP method
                    response = self.get_callback(parsed_message['headers']['request_method'])(parsed_message)
                except SIPStatusCodeError as e:
                    # If a SIPStatusCodeError is raised, return a response with the appropriate status code and reason phrase
                    response = SIPResponseFactory.create_response(status_code=e.status_code, reason_phrase=e.reason_phrase, headers=parsed_message['headers'])
                await self.socket.send(response, address)
        elif isinstance(self.socket, WebSocket):
            # Connect to the WebSocket server
            await self.socket.connect()
            while True:
                data, address = await self.socket.receive()
                parsed_message = SIPParser().parse(data)
                try:
                    # Call the callback function for the SIP method
                    response = self.callbacks[parsed_message['method']](parsed_message)
                except SIPStatusCodeError as e:
                    # If a SIPStatusCodeError is raised, return a response with the appropriate status code and reason phrase
                    response = SIPResponseFactory.create_response(status_code=e.status_code, reason_phrase=e.reason_phrase, headers=parsed_message['headers'])
                await self.socket.send(response, address)
        elif isinstance(self.socket, AsyncTCPSocket):
            # Accept incoming connections
            while True:
                connection, address = await self.socket.accept()
                # Receive data from the connection
                data = await connection.recv(2048, timeout=5)
                parsed_message = SIPParser().parse(data)
                try:
                    # Call the callback function for the SIP method
                    response = self.callbacks[parsed_message['headers']['request_method']](parsed_message)
                except SIPStatusCodeError as e:
                    # If a SIPStatusCodeError is raised, return a response with the appropriate status code and reason phrase
                    response = SIPResponseFactory.create_response(status_code=e.status_code, reason_phrase=e.reason_phrase, headers=parsed_message['headers'])
                await connection.send(response)
