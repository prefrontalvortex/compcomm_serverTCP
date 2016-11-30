class IPHeader(object):
    def __init__(self, version,
                 IHL,
                 TOS,
                 totalLength,
                 id,
                 ipflags,
                 fragoffset,
                 TTL,
                 protocol,
                 sourceAddr,
                 destAddr,
                 ipOption,
                 ):
        pass


class TCPHeader(object):
    def __init__(self, sourcePort,
                 destPort,
                 seqNum,
                 ackNum,
                 offset,
                 reserved=0,
                 tcpflags=0,
                 window=None,
                 checksum=None,
                 urgpointer=0,
                 tcpOptions=0,
                 data=None,
                 ):
        pass


class bits(object):
    def __init__(self, num, length=8):
        if isinstance(num, str):
            self.a = num
        elif isinstance(num, int):
            self.a = bits.binary(num, length)
        else:
            raise TypeError('Cannot convert to binary representation: {}'.format(type(num)))

    def to_stream(self):    return bits.binstr_to_stream(self.a)

    def __add__(self, y):   return bits(self.a + y.a)

    def __len__(self):      return len(self.a)

    def __repr__(self):     return self.a

    @staticmethod
    def binary(num, length=8, spacer=0, pre=''):
        return '{0}{{:{1}>{2}}}'.format(pre, spacer, length).format(bin(num)[2:])

    @staticmethod
    def binstr_to_charlist(binstr):
        charlist = []
        for i in range(0, len(binstr), 8):
            charlist.append(int(binstr[i:i + 8], base=2))
        return charlist

    @staticmethod
    def charlist_to_stream(charlist):
        return ''.join([chr(b) for b in charlist])

    @staticmethod
    def binstr_to_stream(binstr):
        return bits.charlist_to_stream(bits.binstr_to_charlist(binstr))


def port_to_binary(portstr):
    pass

