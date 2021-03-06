'''
    Michael McDermott - Computer Comm Networks
    UDP and TCP echo client
'''
from __future__ import print_function, division
import socket
import time
from header import *

PORT_OUT = 1337
HOST = ''
BUFSIZE=4096
FIN=1
SYN=2
ACK=0x10

class Client(object):
    def __init__(self, host=HOST, port=PORT_OUT):
        self.start = time.time()
        self.host = host
        self.port = port

        socktype = socket.SOCK_DGRAM
        try:
            self.sock = socket.socket(socket.AF_INET, socktype)
        except socket.error as err:
            print('Failed to create socket. Error Code : ' + str(err[0]) + ' Message ' + err[1])
            raise err

        print('{0} Socket bind complete. Host: {1}:{2}'.format('udp', host, port))

    def send(self, message):

        seq_init = 1337
        packet = TCPPacket(data=message, tcpflags=2, seqNum=seq_init, verbose=True)

        self.sock.sendto(packet.bin, (self.host, self.port))
        data, addr = self.sock.recvfrom(BUFSIZE)
        packet = TCPPacket().from_binary(data)

        print('Reply from {0}: \n_____\n{1}\n_____'.format(addr, packet))
        # print('Elapsed: {0}'.format(stop-start))

    def establish(self, message):

        seq_init = 1337
        packet = TCPPacket(data=message, tcpflags=SYN, seqNum=seq_init, verbose=True)

        self.sock.sendto(packet.bin, (self.host, self.port))
        data, addr = self.sock.recvfrom(BUFSIZE)
        packet = TCPPacket().from_binary(data)

        print('Reply from {0}: \n_____\n{1}\n_____'.format(addr, packet))
        packet = TCPPacket(data=message, tcpflags=ACK, seqNum=seq_init, verbose=True)
        self.sock.sendto(packet.bin, (self.host, self.port))

if __name__ == "__main__":
    client = Client()
    client.establish('I am the client')
