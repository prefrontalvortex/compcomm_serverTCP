import socket
import select


TIMEOUT_S = 3
BUFFSIZE = 1024
address = ('localhost', 1337)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
sock.settimeout(3)

# sock.setblocking(0)

# ready = select.select([sock], [], [], TIMEOUT_S)
# if ready[0]:
data = sock.recvfrom(4096)