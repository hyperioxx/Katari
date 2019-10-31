import threading
import socketserver
from Katari.sip import SipMessage


class UDPSipServer(socketserver.DatagramRequestHandler):

    application = None
    settings = None

    def handle(self):
        """

        :return:
        """

        if not UDPSipServer.check_allowed(self.client_address[0]):
            return

        datagram = self.rfile.read()
        message = SipMessage(datagram)
        UDPSipServer.application.socket = self.request
        UDPSipServer.application.client = self.client_address
        UDPSipServer.application._server_run(message, self.client_address)

    @staticmethod
    def start(ServerAddress, applcation):
        """
        Forks application to handle request

        :param ServerAddress:
        :param applcation:
        :return:
        """

        UDPSipServer.application = applcation
        UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress, UDPSipServer)
        UDPServerObject.serve_forever()


    @staticmethod
    def check_allowed(address):
        if len(UDPSipServer.settings.ALLOWED_HOSTS) <= 0:
            return True
        elif address in UDPSipServer.settings.ALLOWED_HOSTS:
            return True
        return False

