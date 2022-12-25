class AcceptHeader:
    def __init__(self, value):
        self.media_ranges = []
        parts = value.split(",")
        for part in parts:
            media_range, *parameters = part.split(";")
            parameters = {param.split("=")[0]: param.split("=")[1] for param in parameters}
            self.media_ranges.append((media_range.strip(), parameters))
    
    def __str__(self):
        media_range_strs = []
        for media_range, parameters in self.media_ranges:
            param_strs = []
            for key, value in parameters.items():
                param_strs.append(f"{key}={value}")
            media_range_strs.append(f"{media_range}; {'; '.join(param_strs)}")
        return f"{', '.join(media_range_strs)}"



class AcceptEncodingHeader:
    def __init__(self, value):
        self.content_coding = []
        parts = value.split(",")
        for part in parts:
            content_coding, *parameters = part.split(";")
            parameters = {param.split("=")[0]: param.split("=")[1] for param in parameters}
            self.content_coding.append((content_coding.strip(), parameters))
    
    def __str__(self):
        content_coding_strs = []
        for content_coding, parameters in self.content_coding:
            param_strs = []
            for key, value in parameters.items():
                param_strs.append(f"{key}={value}")
            content_coding_strs.append(f"{content_coding}; {'; '.join(param_strs)}")
        return f"{', '.join(content_coding_strs)}"


class AcceptLanguageHeader:
    def __init__(self, value):
        self.languages = []
        parts = value.split(",")
        for part in parts:
            language, *parameters = part.split(";")
            parameters = {param.split("=")[0]: param.split("=")[1] for param in parameters}
            self.languages.append((language.strip(), parameters))
    
    def __str__(self):
        language_strs = []
        for language, parameters in self.languages:
            param_strs = []
            for key, value in parameters.items():
                param_strs.append(f"{key}={value}")
            language_strs.append(f"{language}; {'; '.join(param_strs)}")
        return f"{', '.join(language_strs)}"

class AlertInfoHeader:
    def __init__(self, value):
        self.alert_info = []
        parts = value.split(",")
        for part in parts:
            alert_info, *parameters = part.split(";")
            parameters = {param.split("=")[0]: param.split("=")[1] for param in parameters}
            self.alert_info.append((alert_info.strip(), parameters))
    
    def __str__(self):
        alert_info_strs = []
        for alert_info, parameters in self.alert_info:
            param_strs = []
            for key, value in parameters.items():
                param_strs.append(f"{key}={value}")
            alert_info_strs.append(f"{alert_info}; {'; '.join(param_strs)}")
        return f"{', '.join(alert_info_strs)}"



class AllowHeader:
    def __init__(self, value):
        self.methods = [i.strip() for i in value.split(",")]
    
    def __str__(self):
        return f"{', '.join(self.methods)}"


class AuthenticationInfoHeader:
    def __init__(self, value):
        self.nextnonce = None
        self.qop = None
        self.rspauth = None
        self.cnonce = None
        self.nc = None
        self.other_parameters = {}
        
        parts = value.split(";")
        for part in parts:
            if "=" in part:
                key, value = part.split("=")
                if key.lower() == "nextnonce":
                    self.nextnonce = value.strip()
                elif key.lower() == "qop":
                    self.qop = value.strip()
                elif key.lower() == "rspauth":
                    self.rspauth = value.strip()
                elif key.lower() == "cnonce":
                    self.cnonce = value.strip()
                elif key.lower() == "nc":
                    self.nc = value.strip()
                else:
                    self.other_parameters[key.lower()] = value.strip()
            else:
                self.other_parameters[part.lower()] = None
    
    def __str__(self):
        params = []
        if self.nextnonce is not None:
            params.append(f"nextnonce={self.nextnonce}")
        if self.qop is not None:
            params.append(f"qop={self.qop}")
        if self.rspauth is not None:
            params.append(f"rspauth={self.rspauth}")
        if self.cnonce is not None:
            params.append(f"cnonce={self.cnonce}")
        if self.nc is not None:
            params.append(f"nc={self.nc}")


class AuthorizationHeader:
    def __init__(self, value):
        self.scheme = None
        self.realm = None
        self.nonce = None
        self.username = None
        self.uri = None
        self.response = None
        self.algorithm = None
        self.opaque = None
        self.qop = None
        self.nc = None
        self.cnonce = None
        self.other_parameters = {}
        
        parts = value.split(" ")
        self.scheme = parts[0]
        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=")
                if key.lower() == "realm":
                    self.realm = value.strip('"')
                elif key.lower() == "nonce":
                    self.nonce = value.strip('"')
                elif key.lower() == "username":
                    self.username = value.strip('"')
                elif key.lower() == "uri":
                    self.uri = value.strip('"')
                elif key.lower() == "response":
                    self.response = value.strip('"')
                elif key.lower() == "algorithm":
                    self.algorithm = value.strip()
                elif key.lower() == "opaque":
                    self.opaque = value.strip('"')
                elif key.lower() == "qop":
                    self.qop = value.strip()
                elif key.lower() == "nc":
                    self.nc = value.strip()
                elif key.lower() == "cnonce":
                    self.cnonce = value.strip('"')
                else:
                    self.other_parameters[key.lower()] = value.strip('"')
            else:
                self.other_parameters[part.lower()] = None
    
    def __str__(self):
        params = []
        if self.realm is not None:
            params.append(f'realm="{self.realm}"')
        if self.nonce is not None:
            params.append(f'nonce="{self.nonce}"')
        if self.username is not None:
            params.append(f'username="{self.username}"')
        if self.uri is not None:
            params.append(f'uri="{self.uri}"')
        if self.response is not None:
            params.append(f'response="{self.response}"')
        if self.algorithm is not None:
            params.append(f'algorithm={self.algorithm}')
        if self.opaque is not None:
            params.append(f'opaque="{self.opaque}"')
        if self.qop is not None:
            params.append(f'qop={self.qop}')
        if self.nc is not None:
            params.append(f'nc={self.nc}')

        
class ViaHeader:
    def __init__(self, value):
        self.protocol_name = None
        self.protocol_version = None
        self.transport = None
        self.sent_by = None
        self.other_parameters = {}
    
    
    
        parts = value.split(" ")
        self.protocol_name, self.protocol_version, self.transport = parts[0].split("/")
        
        self.sent_by_parts = parts[1].split(":")
        self.sent_by_ip, self.sent_by_port = self.sent_by_parts[0], self.sent_by_parts[1]
        self.sent_by = f"{self.sent_by_ip}:{self.sent_by_port}"
        
        for part in parts[2:]:
            if "=" in part:
                key, value = part.split("=")
                self.other_parameters[key.lower()] = value.strip()
            else:
                self.other_parameters[part.lower()] = None

    def __str__(self):
        params = []
        for key, value in self.other_parameters.items():
            if value is None:
                params.append(key)
            else:
                params.append(f"{key}={value}")
        return f"{self.protocol_name}/{self.protocol_version}/{self.transport} {self.sent_by}; {'; '.join(params)}"


class CallIDHeader:
    def __init__(self, value):
        self.call_id = value
    
    def __str__(self):
        return f"{self.call_id}"

      
class CallInfoHeader:
    def __init__(self, value):
        self.uri = None
        self.other_parameters = {}
        
        parts = value.split(";")
        self.uri = parts[0]
        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=")
                self.other_parameters[key.lower()] = value.strip('"')
            else:
                self.other_parameters[part.lower()] = None
    
    def __str__(self):
        params = []
        for key, value in self.other_parameters.items():
            if value is None:
                params.append(key)
            else:
                params.append(f"{key}={value}")
        return f"{self.uri}; {'; '.join(params)}"



class ContactHeader:
    def __init__(self, value):
        self.name_addr = None
        self.uri = None
        self.display_name = None
        self.other_parameters = {}
        
        parts = value.split(";")
        if " " in parts[0]:
            self.display_name, self.uri = parts[0].split(" ", 1)
            self.name_addr = f"{self.display_name} {self.uri}"
        else:
            self.uri = parts[0]
            self.name_addr = self.uri
        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=")
                self.other_parameters[key.lower()] = value.strip('"')
            else:
                self.other_parameters[part.lower()] = None
    
    def __str__(self):
        params = []
        for key, value in self.other_parameters.items():
            if value is None:
                params.append(key)
            else:
                params.append(f"{key}={value}")
        return f"{self.name_addr}; {'; '.join(params)}"



class CSeqHeader:
    def __init__(self, value):
        self.sequence_number = None
        self.method = None
        
        parts = value.split(" ")
        self.sequence_number = int(parts[0])
        self.method = parts[1]
    
    def __str__(self):
        return f"{self.sequence_number} {self.method}"


class FromHeader:
    def __init__(self, value):
        self.name_addr = None
        self.uri = None
        self.display_name = None
        self.other_parameters = {}
        
        parts = value.split(";")
        if " " in parts[0]:
            self.display_name, self.uri = parts[0].split(" ", 1)
            self.name_addr = f"{self.display_name} {self.uri}"
        else:
            self.uri = parts[0]
            self.name_addr = self.uri
        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=")
                self.other_parameters[key.lower()] = value.strip('"')
            else:
                self.other_parameters[part.lower()] = None
    
    def __str__(self):
        params = []
        for key, value in self.other_parameters.items():
            if value is None:
                params.append(key)
            else:
                params.append(f"{key}={value}")
        return f"{self.name_addr}; {'; '.join(params)}"


class ToHeader:
    def __init__(self, value):
        self.name_addr = None
        self.uri = None
        self.display_name = None
        self.other_parameters = {}
        
        parts = value.split(";")
        if " " in parts[0]:
            self.display_name, self.uri = parts[0].split(" ", 1)
            self.name_addr = f"{self.display_name} {self.uri}"
        else:
            self.uri = parts[0]
            self.name_addr = self.uri
        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=")
                self.other_parameters[key.lower()] = value.strip('"')
            else:
                self.other_parameters[part.lower()] = None
    
    def __str__(self):
        params = []
        for key, value in self.other_parameters.items():
            if value is None:
                params.append(key)
            else:
                params.append(f"{key}={value}")
        return f"{self.name_addr}; {'; '.join(params)}"



class ExpireHeader:
    def __init__(self, value):
        self.delta_seconds = int(value)
    
    def __str__(self):
        return f"{self.delta_seconds}"


class UserAgentHeader:
    def __init__(self, value):
        self.product_tokens = value.split(" ")
    
    def __str__(self):
        return f"{' '.join(self.product_tokens)}"


class MaxForwardsHeader:
    def __init__(self, value):
        self.max_forwards = int(value)
    
    
    def __str__(self):
        return f"{self.max_forwards}"


class ContentLengthHeader:
    def __init__(self, value):
        self.content_length = int(value)
    
    def __str__(self):
        return f"{self.content_length}"


