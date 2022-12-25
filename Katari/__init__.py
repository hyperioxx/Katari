from abc import ABC, abstractmethod

from Katari.sockets import create_socket, AsyncTCPSocket, WebSocket, AsyncUDPSocket
from Katari.sip.parser import SIPParser, SIPStatusCodeError, SIPResponseFactory, SIPTransaction

class SIPServerFactory:
    def create_server(self, server_type, socket_type, host, port):
        """
        Creates a new SIP server instance.
    
        :param server_type: the type of SIP server to create (either "stateless" or "stateful")
        :type server_type: str
        :param socket_type: the type of socket to use for the server (e.g. "udp", "tcp", or "websocket")
        :type socket_type: str
        :param host: the hostname or IP address to bind the server to
        :type host: str
        :param port: the port number to bind the server to
        :type port: int
        :return: a new SIP server instance
        :rtype: StatelessSIPServer or StatefulSIPServer
        """
        if server_type == "stateless":
            return StatelessSIPServer(socket_type, host, port)
        elif server_type == "stateful":
            return StatefulSIPServer(socket_type, host, port)
        else:
            raise ValueError("Invalid server type: {}".format(server_type))

class SIPServer(ABC):
    """
    An interface for SIP servers.
    """
    @abstractmethod
    def register_callback(self, method, callback):
        """
        Register a callback function for a SIP method.

        :param method: The SIP method to register the callback for.
        :type method: str
        :param callback: The callback function to register.
        :type callback: function
        """
        pass

    @abstractmethod
    def get_callback(self, method):
        """
        Get the callback function for a SIP method.

        :param method: The SIP method to get the callback for.
        :type method: str
        :return: The callback function for the specified SIP method.
        :rtype: function
        """
        pass

    @abstractmethod
    async def run(self):
        """
        Run the SIP server.
        """
        pass


class StatelessSIPServer(SIPServer):
    def __init__(self, socket_type, host, port):
        self.host = host
        self.port = port
        self.socket = create_socket(socket_type, host, port)
        self.callbacks = {}

    def register_callback(self, method):
        def decorator(func):
            self.callbacks[method] = func
            return func
        return decorator

    def get_callback(self, method):
        try:
            return self.callbacks[method] 
        except KeyError:
            raise SIPStatusCodeError(status_code=501, reason_phrase="Not Implemented")


    async def run(self):
        while True:
            # Receive incoming data from the socket
            data, address = await self.socket.receive()
    
            # Parse the incoming SIP message
            parsed_message = SIPParser().parse(data)
    
            # Get the callback function for the SIP method of the incoming message
            callback = self.get_callback(parsed_message["start_line"]["method"])
    
            # Call the callback function with the incoming message
            response = callback(parsed_message)
    
            # Send the response back to the client
            await self.socket.send(response, address)
            

class StatefulSIPServer(SIPServer):
    def __init__(self, socket_type, host, port):
        self.host = host
        self.port = port
        self.socket = create_socket(socket_type, host, port)
        self.callbacks = {}
        self.transactions = {}

    def register_callback(self, method):
        def decorator(func):
            self.callbacks[method] = func
            return func
        return decorator

    def get_callback(self, method):
        try:
            return self.callbacks[method] 
        except KeyError:
            raise SIPStatusCodeError(status_code=501, reason_phrase="Not Implemented")

    def get_transaction(self, message):
        if message['start_line']["type"] == "request":
            transaction = SIPTransaction(self, message)
            self.transactions[transaction.id] = transaction
            return transaction
        elif message["type"] == "response":
            try:
                return self.transactions[message["via"]["branch"]]
            except KeyError:
                raise SIPStatusCodeError(status_code=481, reason_phrase="Transaction Does Not Exist")

    async def run(self):
        while True:
            # Receive incoming data from the socket
            data, address = await self.socket.receive()
    
            # Parse the incoming SIP message
            parsed_message = SIPParser().parse(data)
    
            # Get the transaction for the incoming message
            transaction = self.get_transaction(parsed_message)
    
            # Handle the incoming message
            response = transaction.handle_message(parsed_message)
    
            # Send the response, if any
            if response:
                await self.socket.send(response, address)
    

            
