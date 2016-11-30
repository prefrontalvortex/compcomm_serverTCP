'''
    Michael McDermott - Computer Comm Networks
    UDP and TCP echo client
'''
from __future__ import print_function, division
import socket
import time

PORT_OUT = 1337
HOST = ''

def send(message, host, port, proto='udp'):
    if proto == 'udp':
        socktype = socket.SOCK_DGRAM
    elif proto == 'tcp':
        socktype = socket.SOCK_STREAM
    else:
        raise NotImplementedError('Invalid configuration: {0}'.format(proto))

    try:
        sock = socket.socket(socket.AF_INET, socktype)
    except socket.error as err:
        print('Failed to create socket. Error Code : ' + str(err[0]) + ' Message ' + err[1])
        raise err

    print('{0} Socket bind complete. Host: {1}:{2}'.format(proto, host, port))

    start = time.time()
    if proto == 'udp':
        sock.sendto(str.encode(message), (host, port))
    elif proto == 'tcp':
        sock.connect((host, port))
        sock.send(str.encode(message))
    data, addr = sock.recvfrom(config.BUFSIZE)
    addr = host
    sock.close()
    stop = time.time()
    print('Reply from {0}: \n_____\n{1}\n_____'.format(addr, str.decode(data)))
    print('Elapsed: {0}'.format(stop-start))


if __name__ == "__main__":
    proto = 'tcp'
    send('Hello {0} server!'.format(proto), PORT_OUT, proto)
