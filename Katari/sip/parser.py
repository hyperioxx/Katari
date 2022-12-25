from Katari.sip.headers import *

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
        body = f"\r\n\r\n{content}" if content else "\r\n\r\n"
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
        self.request_methods = ["INVITE", "ACK", "OPTIONS", "BYE", "CANCEL", "REGISTER", "SUBSCRIBE", "NOTIFY", "PUBLISH", "INFO", "REFER", "MESSAGE"]
        
    def parse(self, message: bytes):
        # Split the message into lines
        message = message.decode()
        lines = message.split("\r\n")
        
        # Parse the start line
        start_line = lines[0]
        start_line_parts = start_line.split(" ")
        if start_line_parts[0] in self.request_methods:
            # It's a request
            method = start_line_parts[0]
            uri = start_line_parts[1]
            version = start_line_parts[2]
            start_line = {
                "type": "request",
                "method": str(method),
                "uri": str(uri),
                "version": str(version),
            }
        elif start_line_parts[0] == "SIP/2.0":
            # It's a response
            version = start_line_parts[0]
            status_code = start_line_parts[1]
            reason_phrase = " ".join(start_line_parts[2:])
            start_line = {
                "type": "response",
                "version": version,
                "status_code": status_code,
                "reason_phrase": reason_phrase,
            }
        else:
            raise ValueError("Invalid start line")
        
        # Parse the headers
        headers = {}
        current_header_name = None
        current_header_value = []
        for line in lines[1:]:
            if not line:
                # End of headers
                break
            if line[0] in " \t":
                # Continuation of previous header
                current_header_value.append(line.strip())
            else:
                # New header
                if current_header_name is not None:
                    # Save the previous header
                    headers[current_header_name] = self.parse_header(current_header_name, " ".join(current_header_value))
                parts = line.split(":", 1)
                current_header_name = parts[0]
                current_header_value = [parts[1].strip()]
        if current_header_name is not None:
            # Save the last header
            headers[current_header_name] = self.parse_header(current_header_name, " ".join(current_header_value))
        
        # Get the body
        body = "\n".join(lines[len(headers)+1:])
        
        # Return the parsed message
        return {
            "start_line": start_line,
            "headers": headers,
            "body": body,
        }
    
    def parse_header(self, name, value):
        name = name
        if name == "Accept":
            return AcceptHeader(value)
        elif name == "Accept-Encoding":
            return AcceptEncodingHeader(value)
        elif name == "Accept-Language":
            return AcceptLanguageHeader(value)
        elif name == "Alert-Info":
            return AlertInfoHeader(value)
        elif name == "Allow":
            return AllowHeader(value)
        elif name == "Authentication-Info":
            return AuthenticationInfoHeader(value)
        elif name == "Authorization":
            return AuthorizationHeader(value)
        elif name == "Call-ID":
            return CallIDHeader(value)
        elif name == "Call-Info":
            return CallInfoHeader(value)
        elif name == "Contact":
            return ContactHeader(value)
        elif name == "CSeq":
            return CSeqHeader(value)
        elif name == "From":
            return FromHeader(value)
        elif name == "Via":
            return ViaHeader(value)
        elif name == "To":
            return ToHeader(value)
        elif name == "Expires":
            return ExpireHeader(value)
        elif name == "User-Agent":
            return UserAgentHeader(value)
        elif name == "Max-Forwards":
            return MaxForwardsHeader(value)
        elif name == "Content-Length":
            return ContentLengthHeader(value)
        else:
            return value
        




class SIPTransaction:
    def __init__(self, message, server):
        self.server = server
        self.request = message
        self.response = None
        self.completed = False

    def get_callback(self):
        try:
            return self.server.get_callback(self.request["method"])
        except KeyError:
            raise SIPStatusCodeError(status_code=501, reason_phrase="Not Implemented")

    def create_response(self, status_code, reason_phrase, headers=None, content=b''):
        headers = headers or {}
        headers["request_method"] = self.request["method"]
        headers["request_uri"] = self.request["uri"]
        headers["sip_version"] = self.request["version"]
        return SIPResponseFactory.create_response(status_code, reason_phrase, headers, content)

    def handle_message(self, message):
        if message["type"] == "request":
            if self.request:
                # It's a retransmission of the request
                return self.response
            else:
                # It's a new request
                self.request = message
                # Get the callback function for the SIP method
                callback = self.get_callback()
                # Call the callback function with the request
                self.response = callback(self.request)
                return self.response
        elif message["type"] == "response":
            if self.response:
                # It's a retransmission of the response
                return
            else:
                # It's a new response
                self.response = message
                self.completed = True
        else:
            raise ValueError("Invalid message type")
