'''
    Michael McDermott - Computer Comm Networks
    UDP and TCP echo server
'''
import socket
import time
import random


class Server(object):
    def __init__(self, host, port, proto='udp', delay=False):
        self.setup(host, port, proto, delay)

    def setup(self, host, port, proto='udp', delay=False):
        self.proto = proto
        self.delay = delay
        self.port = port
        self.host = host

        # Datagram (udp) socket: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # TCP socket: socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if proto == 'udp':
            socktype = socket.SOCK_DGRAM
        elif proto == 'tcp':
            socktype = socket.SOCK_STREAM
        else:
            raise NotImplementedError('Invalid configuration: {0}'.format(proto))

        try:
            self.sock = socket.socket(socket.AF_INET, socktype)
            print('Socket created')
        except socket.error as err:
            print('Failed to create socket. Error Code : ' + str(err[0]) + ' Message ' + err[1])
            raise err

        try:
            self.sock.bind((host, port))
        except socket.error as err:
            print('Bind failed. Error Code : ' + str(err[0]) + ' Message ' + err[1])
            raise err

        if proto == 'tcp':
            self.sock.listen(config.BACKLOG)

        print('{0} Socket bind complete. Host: {1}:{2}'.format(proto, host, port))
        try:
            self.run()
        except KeyboardInterrupt:
            print('terminated\n')
        except socket.error as err:
            print('___{0}___'.format(err[0]))
        finally:
            self.sock.close()


    def run(self):

        while 1:
            # receive data from client (data, addr)
            try:
                if self.proto == 'udp':
                    data, addr = self.sock.recvfrom(config.BUFSIZE)
                elif self.proto == 'tcp':
                    client, address = self.sock.accept()
                    data = client.recv(config.BUFSIZE)
                    addr = self.host
            except KeyboardInterrupt:
                print('!keyboard interrupt, terminating\n')
                self.sock.close()
                break
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
            if self.delay:
                delaytime = random.randint(1,10)
                print('Sleeping for {0} s'.format(delaytime))
                time.sleep(delaytime)
            else:
                delaytime = 0


            if self.proto == 'udp':
                self.sock.sendto(reply, addr)
            elif self.proto == 'tcp':
                client.send(reply)


if __name__ == "__main__":
    proto = 'tcp'
    delay = False
    server = Server(config.HOST, config.PORT_OUT, proto, delay)
    server.run()