from Katari.sip import SipMessage


class MultipleChoices300(SipMessage):
    def __init__(self):
        super().__init__()
        self.method_line = "SIP/2.0 300 Multiple Choices\r\n"


class MovedPermanently301(SipMessage):
    def __init__(self):
        pass


class MovedTemporarily302(SipMessage):
    def __init__(self):
        super().__init__()
        self.method_line = "SIP/2.0 302 Moved Temporarily\r\n"

    def append_contact(self, contact, weight):
        def create_sip_uri(contact, weight):
            return "<sip:{}>;q={}".format(contact, weight)
        if self._data["contact"]:
            self._data["contact"] = self._data["contact"] + "," + create_sip_uri(contact, weight)
        else:
            self._data["contact"] = self._data["contact"] + create_sip_uri(contact, weight)

    def clean_contact(self):
        self._data["contact"] = ""




class UseProxy305(SipMessage):
    def __init__(self):
        pass


class AlternativeService380(SipMessage):
    def __init__(self):
        pass
