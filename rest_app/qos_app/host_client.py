import socket, optparse
import time
import sys

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='192.168.1.100')
parser.add_option('-p', dest='port', type='int', default=7070)
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((options.ip, options.port))

MESSAGE = 'Get Queue Stats'
BUFFER_SIZE = 1024

try:
    while True:
        time.sleep(2)
        s.sendall(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        print "\nreceived data:\n", data
except KeyboardInterrupt:
    s.close()
    sys.exit(1)