import socket

class TCPTimeoutException(socket.timeout):
    def __init__(self):
        super(TCPTimeoutException, self).__init__()


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


class TCPPacket(object):
    def __init__(self,
                 sourcePort=0xABCD,
                 destPort=0xEF12,
                 seqNum=0,
                 ackNum=0,
                 offset=6,
                 reserved=0xF,
                 tcpflags=0,
                 window=0x9999,
                 checksum=0xDEAD,
                 urgpointer=0xABCD,
                 tcpOptions=0x55555555,
                 data='fabababa', packet=None, verbose=False
                 ):
        self.sourcePort = bits(0,16)
        self.destPort = bits(0,16)
        self._seqNum = bits(0, 32)
        self._ackNum = bits(0, 21)
        self.offset = bits(0,4)
        self.reserved = bits(0,4)
        self.tcpflags = bits(0,8)
        self.window = bits(0,16)
        self.checksum = bits(0,16)
        self.urgpointer = bits(0,16)
        self.tcpOptions = bits(0,32)
        self.data = ''
        if packet is not None: # handle parsing packet as bytestream string
            print packet
            self.parse(packet, verbose)
        else:
            sourcePort = bits(sourcePort, 16)
            destPort = bits(destPort, 16)
            seqNum = bits(seqNum, 32)
            ackNum = bits(ackNum, 32)
            offset = bits(offset, 4)
            reserved = bits(reserved, 4)
            tcpflags = bits(tcpflags, 8)
            window = bits(window, 16)
            checksum = bits(checksum, 16)
            urgpointer = bits(urgpointer, 16)
            tcpOptions = bits(tcpOptions, 32)
            self.sourcePort = sourcePort
            self.destPort = destPort
            self._seqNum = seqNum
            self._ackNum = ackNum
            self.offset = offset
            self.reserved = reserved
            self.tcpflags = tcpflags
            self.window = window
            self.checksum = checksum
            self.urgpointer = urgpointer
            self.tcpOptions = tcpOptions
            self.data = data
            header = self.make_header()
            packet = self.make_packet()
            if verbose:
                print len(header), len(header)/8, len(header)%8, '\n', header


    def make_header(self):
        self.header = self.sourcePort + self.destPort + self._seqNum + self._ackNum + self.offset + self.reserved \
                      + self.tcpflags + self.window + self.checksum + self.urgpointer + self.tcpOptions
        return self.header

    def make_packet(self):
        header_str = self.header.to_stream()
        self._packet = header_str + self.data
        return self.bin

    @property
    def seqnum(self): return self._seqNum.to_int()

    @property
    def acknum(self): return self._ackNum.to_int()

    @property
    def syn(self): return ((self.tcpflags & 2) >> 1).to_int()

    @property
    def ack(self): return ((self.tcpflags & 0x10) >> 4).to_int()

    @property
    def fin(self): return (self.tcpflags & 1)

    def set_ack(self, bitset=1): self.tcpflags = self.tcpflags | 0x10
    def set_push(self, bitset=1): self.tcpflags = self.tcpflags | 8
    def set_reset(self, bitset=1): self.tcpflags = self.tcpflags | 4
    def set_syn(self, bitset=1): self.tcpflags = self.tcpflags | 2
    def set_fin(self, bitset=1): self.tcpflags = self.tcpflags | 1



    @property
    def bin(self): return self._packet

    @property
    def hex(self):
        return [hex(ord(c))[2:] for i,c in enumerate(self.bin)]

    @staticmethod
    def from_binary(packet):
        return TCPPacket(packet=packet)

    def parse(self, packet, verbose=False):

        offset_reserved = ord(packet[12])
        offset = (offset_reserved & 0xF0) >> 4
        if verbose: print('offset: ', offset, offset*4)
        data = packet[offset*4:]
        if verbose: print data
        self.data = data
        self.sourcePort = bits(short(packet[:2]))
        self.destPort = bits(short(packet[2:4]))
        self._seqNum = bits(sint(packet[4:8]))
        self._ackNum = bits(sint(packet[8:12]))
        self.offset = bits(offset)
        self.reserved = bits((offset_reserved & 0xF))
        self.tcpflags = bits(numa(packet[13]))
        self.window = bits(numa(packet[14:16]))
        self.checksum = bits(numa(packet[16:18]))
        self.urgpointer = bits(numa(packet[18:20]))



        return data

    def __str__(self):
        rep = 'Source port: {0}\nDestination port: {1}\nSequence Num: {2}\nAcknowledgeNum: {3}\n'.format(
            self.sourcePort.to_int(), self.destPort.to_int(), self._seqNum.to_int(), self._ackNum.to_int())
        rep = rep + 'Window: {0}\nChecksum: {1}\nTCP Options: {2}\n'.format(
            self.window, self.checksum, self.tcpOptions)
        rep = rep + 'Flags: {0:0>8}\n'.format(bin(self.tcpflags.to_int())[2:])
        rep = rep + 'Ack: {0}\n'.format(self.ack)
        rep = rep + 'Syn: {0}\n'.format(self.syn)
        rep = rep + 'Data: {0}\n'.format(self.data)
        return rep

def short(bytes):
    assert len(bytes) == 2, 'Cannot parse Short from bytestring'
    return ord(bytes[0])*256 + ord(bytes[1])

def sint(bytes):
    assert len(bytes) == 4, 'Cannot parse Int from bytestring'
    val = 0
    for i in range(4):
        val += ord(bytes[i]) * 256**(3-i)
    return val

def numa(bytes):
    l = len(bytes)
    val = 0
    for i in range(l):
        val += ord(bytes[i]) * 256**(l-1-i)
    return val


class Timeout():
    pass

class bits(object):
    def __init__(self, num, length=8):
        if isinstance(num, str):
            self.a = num
        elif isinstance(num, int):
            self.a = bits.binary(num, length)
        else:
            raise TypeError('Cannot convert to binary representation: {0}'.format(type(num)))

    def to_stream(self):    return bits.binstr_to_stream(self.a)

    def to_int(self):       return numa(self.to_stream())

    def __add__(self, y):   return bits(self.a + y.a)

    def __xor__(self, other): return bits(self.to_int() ^ other)

    def __and__(self, other): return bits(self.to_int() & other)

    def __or__(self, other): return bits(self.to_int() | other)

    def __lshift__(self, other): return bits(self.to_int() << other)

    def __rshift__(self, other): return bits(self.to_int() >> other)


    def __len__(self):      return len(self.a)

    def __repr__(self):     return self.a

    @staticmethod
    def binary(num, length=8, spacer=0, pre=''):
        return '{0}{{0:{1}>{2}}}'.format(pre, spacer, length).format(bin(num)[2:])

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

