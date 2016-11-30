'''
    Michael McDermott - Computer Comm Networks
    UDP and TCP echo server
'''
import sys
import socket
import time
import random
from header import *

PORT_OUT = 1337
HOST = 'localhost'
BACKLOG = 5
ENCODING = 'utf-8'
BUFSIZE = 1024
TIMEOUT_S = 1


class Server(object):
    def __init__(self, host, port, timeout=9, delay=False):
        self.packets=[]
        self.setup(host, port, timeout, delay)

    def setup(self, host, port, timeout=1, delay=False):
        self.proto = proto
        self.delay = delay
        self.port = port
        self.host = host
        self.timeout = timeout

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as err:
            print('Failed to create socket. Error Code : ' + str(err[0]) + ' Message ' + err[1])
            raise err
        self.sock.bind((host, port))
        self.sock.settimeout(1)


        print('{0} Socket bind complete. Host: {1}:{2}'.format(proto, host, port))
        try:
            self.run()
            # sock.recvfrom(4096)
            pass
        except KeyboardInterrupt:
            print('terminated\n')
        # except socket.error as err:
        #     print('socket run error ___{0}___'.format(err[0]))
        finally:
            self.sock.close()


    def run(self):
        data, addr = None, None
        while 1:
            test = self.s_listen()
            test = self.s_syn_sent()

    def state_caller(self):
        pass


    def s_closed(self):
        pass

    def listen_for(self, timeout=False, verbose=False):
        listening=True
        data, addr = None, None
        while listening:
            # receive data from client (data, addr)
            try:
                data, addr = self.sock.recvfrom(BUFSIZE)

            except KeyboardInterrupt:
                print('!keyboard interrupt, terminating\n')
                self.sock.close()
                sys.exit(1)
                break
            except socket.timeout as err:
                if verbose: print('Timeout')
                if timeout: return Timeout()
            except socket.error as err:
                if err[0] == 9:
                    self.sock.close()
                    break
                else:
                    raise err

            if data:
                return data, addr

    def s_listen(self, verbose=False):
        # Listening for packet
        data, addr = None, None
        while 1:
            response = self.listen_for()
            if isinstance(response, tuple):
                data, addr = response

            if data:
                print('Incoming from: {0}'.format(addr))
                packet = TCPPacket().from_binary(data)
                self.packets.append(packet)
                self.addr = addr
                print('_____\n{0}\n_____'.format(packet))
                reply = TCPPacket(tcpflags=2, seqNum=1, ackNum=0, data='I am server')
                self.sock.sendto(reply.bin, addr)
                return 1


    def s_established(self):
        # TCP connection established
        pass

    def s_syn_rcvd(self):
        pass

    def s_syn_sent(self):
        data, addr = None, None
        while 1:
            response = self.listen_for()
            if isinstance(response, tuple):
                data, addr = response

            if data:
                print('Incoming from: {0}'.format(addr))
                packet = TCPPacket().from_binary(data)
                print('_____\n{0}\n_____'.format(packet))
                reply = TCPPacket(tcpflags=0x12, seqNum=1, ackNum=0, data='I am server')
                self.sock.sendto(reply.bin, addr)
                return 1

    def s_fin_wait_1(self):
        pass

    def s_fin_wait_2(self):
        pass

    def s_time_wait(self):
        pass



if __name__ == "__main__":

    proto = 'udp'
    delay = False
    server = Server(HOST, PORT_OUT)
    server.run()
    # packet = TCPPacket(0xBEBE, 0xCECE, 0xACE1CA72, 0xACE1CA72, verbose=0)
    # print packet.bin
    # print packet.hex
    # print TCPHeader().parse(packet=packet.bin)
    # pack2 = TCPPacket.from_binary(packet.bin)
    # pack2.set_syn()
    # print pack2
