"""
Utils module containing all sip header classes
"""
import re
import logging
from collections import OrderedDict
from Katari.errors import *



class Message:
    """
    Base message
    """
    def __init__(self, message):
        self.raw_message = message
        self._data = OrderedDict()
        self.log = logging.getLogger('Katari')
        if message:
            self.method_line, self.headers = message.decode().split("\r\n", 1)
            self._parser(self.headers)
            self.sip_type = self.get_method(self.method_line)

    def __getitem__(self, item):
        """
        :param item:
        :return:
        """
        try:
            return self._data[item]
        except KeyError:
            return None

    def _parser(self, message):
        """
        :param message:
        :return:
        """
        reg=re.compile('([a-zA-Z-]+):(.*)')
        for header, value in dict(reg.findall(message)).items():
            value = value.replace('\n\r', '')
            try:
                if header.lower() == "to":
                    self._data[header.lower()] = URI(value)
                elif header.lower() == "from":
                    self._data[header.lower()] = URI(value)
                elif header.lower() == "contact":
                    self._data[header.lower()] = URI(value)
                else:
                    self._data[header.lower()] = value
            except Exception as err:
                self.log.exception(err)
                self.log.debug(header, value)

    def get_method(self, methodline):
        """
        :param methodline:
        :return:
        """
        try:
            return methodline.split()[0]
        except:
            pass


class URI:
    """

    """
    def __init__(self, uri):
        self.log = logging.getLogger('Katari')
        self.uri = uri
        self.expression = re.compile(
                    '(?P<scheme>\w+):' 
                    +'(?:(?P<user>[+\w\.\-]+):?(?P<password>[\w\.]+)?@)?'
                    +'\[?(?P<host>' 
                        +'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|' 
                        +'(?:(?:[0-9a-fA-F]{1,4}):){7}[0-9a-fA-F]{1,4}|' 
                        +'(?:(?:[0-9A-Za-z]+\.)+[0-9A-Za-z]+)'
                    +')\]?:?' 
                    +'(?P<port>\d{1,6})?' 
                    +'(?:\;(?P<params>[^\?]*))?' 
                    +'(?:\?(?P<headers>.*))?' 
        )
        try:
            self.user = self.expression.search(uri).group('user')
        except:
            self.log.info("Unable to find user in URI: {}".format(uri))
        try:
            self.params = self.expression.search(uri).group('params')
        except:
            self.log.info("Unable to find params in URI: {}".format(uri))
        try:
            self.address = self.expression.search(uri).group('host')
        except:
            self.log.info("Unable to find host in URI: {}".format(uri))
        try:
            self.port = self.expression.search(uri).group('port')
        except:
            self.log.info("Unable to find port in URI: {}".format(uri))

    def __repr__(self):
        return self.uri

    def __str__(self):
        return str(self.uri)

    def get_address(self):
        return self.address

    def get_user(self):
        return self.user


class Allow:
    def __init__(self, values):
        pass

class Via:
    def __init__(self):
        pass

class CallId:
    def __init__(self):
        pass

class From:
    def __init__(self):
        pass

class To:
    def __init__(self):
        pass


