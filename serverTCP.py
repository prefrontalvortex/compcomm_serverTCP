'''
    Michael McDermott - Computer Comm Networks
    UDP and TCP echo server
'''
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
    def __init__(self, host, port, timeout=1, delay=False):
        self.setup(host, port, timeout, delay)
        # self.tim()

    def tim(self):
        BUFFSIZE = 1024
        address = ('localhost', 1337)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(address)
        sock.settimeout(TIMEOUT_S)

        data = sock.recvfrom(4096)

    def setup(self, host, port, timeout=1, delay=False):
        self.proto = proto
        self.delay = delay
        self.port = port
        self.host = host
        self.timeout = timeout

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
            # receive data from client (data, addr)
            try:
                data, addr = self.sock.recvfrom(BUFSIZE)

            except KeyboardInterrupt:
                print('!keyboard interrupt, terminating\n')
                self.sock.close()
                break
            except socket.timeout as err:
                print('Timeout occured!')
            except socket.error as err:
                if err[0] == 9:
                    self.sock.close()
                    break
                else:
                    raise err

            if not data:
                break
            print('Incoming from: {0}'.format(addr))
            print('_____\n{0}\n_____'.format(str.decode(data)))

            reply = data
            # if self.delay:
            #     delaytime = random.randint(1,10)
            #     print('Sleeping for {0} s'.format(delaytime))
            #     time.sleep(delaytime)
            # else:
            #     delaytime = 0


            if self.proto == 'udp':
                self.sock.sendto(reply, addr)
            # elif self.proto == 'tcp':
            #     client.send(reply)

def tim():
    TIMEOUT_S = 3
    BUFFSIZE = 1024
    address = ('localhost', 1337)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)
    sock.settimeout(3)

    data = sock.recvfrom(4096)

if __name__ == "__main__":

    proto = 'udp'
    delay = False
    server = Server(HOST, PORT_OUT)
    server.run()
    #
    # TIMEOUT_S = 3
    # BUFFSIZE = 1024
    # address = ('localhost', 1337)
    #
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind(address)
    # sock.settimeout(3)

    # data = sock.recvfrom(4096)
    # tim()