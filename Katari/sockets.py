import socket
import asyncio
import websockets

def create_socket(type, host, port):
    """
    Create a socket of the specified type.

    :param type: The type of socket to create. Can be 'udp', 'tcp', or 'websocket'.
    :type type: str
    :param host: The host to bind the socket to.
    :type host: str
    :param port: The port to bind the socket to.
    :type port: int
    :return: An instance of the corresponding socket class.
    :rtype: Socket
    :raises ValueError: If the specified socket type is invalid.

    :Example:

    >>> udp_socket = create_socket('udp', 'localhost', 8000)
    >>> tcp_socket = create_socket('tcp', 'localhost', 8000)
    >>> websocket = create_socket('websocket', 'localhost', 8000)
    """
    if type == 'udp':
        return AsyncUDPSocket(host, port)
    elif type == 'tcp':
        return AsyncTCPSocket(host, port)
    elif type == 'websocket':
        return WebSocket(host, port)
    else:
        raise ValueError(f'Invalid socket type: {type}')


# Define the interface
class Socket:
    def send(self, data):
        """
        Send data through the socket.

        :param data: The data to send.
        :type data: bytes
        :raises NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError
    
    def receive(self):
        """
        Receive data from the socket.

        :return: The received data.
        :rtype: bytes
        :raises NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

class AsyncUDPSocket(Socket):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    async def send(self, data, address):
        self.sock.sendto(data, address)

    async def receive(self):
        data, address = self.sock.recvfrom(4096)
        return data, address
    

class AsyncTCPSocket(Socket):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.conn = None

    async def send(self, data, address=None):
        if address:
            self.sock.sendto(data, address)
        else:
            self.conn.send(data)

    async def receive(self, address=None):
        if address:
            data, _ = self.sock.recvfrom(4096)
        else:
            data = await self.loop.sock_recv(self.conn, 4096)
        return data

    async def accept(self):
        self.conn, self.addr = await self.loop.sock_accept(self.sock)
        return self.conn, self.addr

class WebSocket(Socket):
    def __init__(self, host, port):
        """
        Initialize a WebSocket.

        :param host: The host to connect the WebSocket to.
        :type host: str
        :param port: The port to connect the WebSocket to.
        :type port: int
        """
        self.host = host
        self.port = port
        self.websocket = None
    
    async def connect(self):
        """
        Connect the WebSocket to the specified host and port.
        """
        self.websocket = await websockets.connect(f'ws://{self.host}:{self.port}')
    
    async def send(self, data):
        """
        Send data through the WebSocket.

        :param data: The data to send.
        :type data: bytes
        """
        await self.websocket.send(data)
    
    async def receive(self):
        """
        Receive data from the WebSocket.

        :return: The received data.
        :rtype: bytes
        """
        return await self.websocket.recv()

