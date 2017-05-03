from dnslib import DNSRecord, RCODE
from dnslib.server import BaseResolver
from utils import is_blacked


class Resolver(BaseResolver):

    def __init__(self, addr, port, black_code, blacklist):
        self.addr = addr
        self.port = port
        self.black_code = black_code
        self.blacklist = blacklist

    def resolve(self, request, handler):
        for question in request.questions:
            if is_blacked(question.qname, self.blacklist):
                reply = request.reply()
                reply.header.rcode = getattr(RCODE, self.black_code)
                return reply

        if handler.protocol == 'tcp':
            response = request.send(self.addr, self.port, tcp=True)
        else:
            response = request.send(self.addr, self.port)

        return DNSRecord.parse(response)

