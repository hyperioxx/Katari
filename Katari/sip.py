import re


class SIPResponseFactory:
    @staticmethod
    def create_response(status_code, reason_phrase, headers=None, content=b''):
        """
        Create a SIP response message.

        :param status_code: The status code of the response.
        :type status_code: int
        :param reason_phrase: The reason phrase of the response.
        :type reason_phrase: str
        :param headers: The headers of the response (optional).
        :type headers: dict
        :param content: The content of the response (optional).
        :type content: bytes
        :return: The SIP response message.
        :rtype: bytes
        """
        if headers is None:
            headers = {}
        # Create the start line of the response
        start_line = f"SIP/2.0 {status_code} {reason_phrase}"
        # Create the header lines of the response
        header_lines = "\r\n".join([f"{name}: {value}" for name, value in headers.items() if name not in ['request_method', 'request_uri', 'sip_version']])
        # Create the content of the response
        body = f"\r\n\r\n{content}" if content else ""
        # Return the response message as bytes
        return f"{start_line}\r\n{header_lines}\r\n{body}".encode()



class SIPStatusCodeError(Exception):
    def __init__(self, status_code: int, reason_phrase: str):
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.message = f'SIP status code {status_code} ({reason_phrase})'

    def __str__(self):
        return self.message

class SIPParser:
    def __init__(self):
        self.state = 'start'
        self.header_name = ''
        self.header_value = ''
        self.headers = {}
        self.content = b''

    def parse(self, message: bytes) -> dict:
        """
        Parse a SIP message and return a dictionary of its headers and content.

        :param message: The SIP message to parse, in bytes form.
        :type message: bytes
        :return: A dictionary of the parsed SIP message's headers and content.
        :rtype: dict
        """
        self.state = 'start'
        self.headers = {}
        self.content = b''

        # Iterate over the lines in the message
        for line in message.split(b'\r\n'):
            # Process the line based on the current state
            if self.state == 'start':
                self._parse_start_line(line)
            elif self.state == 'headers':
                self._parse_header_line(line)
            elif self.state == 'content':
                self._parse_content_line(line)

        # Return the parsed headers and content
        return {'headers': self.headers, 'content': self.content}

    def _parse_start_line(self, line: bytes):
        """
        Parse the start line of a SIP message.

        :param line: The start line of the SIP message.
        :type line: bytes
        """
        # Extract the request method, request URI, and SIP version from the start line
        match = re.match(b'^(\\S+) (\\S+) SIP/(\\S+)$', line)
        if match:
            self.headers['request_method'] = match.group(1).decode()
            self.headers['request_uri'] = match.group(2).decode()
            self.headers['sip_version'] = match.group(3).decode()
            self.state = 'headers'

    def _parse_header_line(self, line: bytes):
        """
        Parse a header line of a SIP message.

        :param line: The header line of the SIP message.
        :type line: bytes
        """
        # Check if the line is empty, indicating the end of the headers
        if line == b'':
            self.state = 'content'
        else:
            # Split the line into a header name and value
            match = re.match(b'^(\\S+):(.*)$', line)
            if match:
                self.header_name = match.group(1).decode().lower()
                self.header_value = match.group(2).strip().decode()
                self.headers[self.header_name] = self.header_value

    def _parse_content_line(self, line: bytes) -> tuple:
        """
        Parse a content line of a SIP message.
    
        :param line: The content line to parse.
        :type line: bytes
        :return: A tuple containing the header and value of the content line.
        :rtype: tuple
        """
        # Initialize variables
        header = b''
        value = b''
        in_header = True
    
        # Iterate through the characters of the line
        for c in line:
            if in_header:
                # If we are in the header, append the character to the header unless it is a ':'
                if c == b':':
                    in_header = False
                else:
                    header += c
            else:
                # If we are in the value, append the character to the value
                value += c
    
        # Return the header and value
        return header, value
