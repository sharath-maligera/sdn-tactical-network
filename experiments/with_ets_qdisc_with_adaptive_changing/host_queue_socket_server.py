import socket, optparse
import sys
import subprocess

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='192.168.1.100')
parser.add_option('-p', dest='port', type='int', default=7070)
(options, args) = parser.parse_args()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( (options.ip, options.port) )
    s.listen(5)
except socket.error as error:
    print 'Error while creating socket: {error}'.format(error=error)
    sys.exit(1)

try:
    conn, addr = s.accept()
    while True:
        try:
            data = conn.recv(1024)
            if data == 'Get Queue Stats':
                print 'Get Queue Stats: message received'
                return_value = subprocess.check_output(['tc', '-s', '-j', 'qdisc', 'show', 'dev', 'r1-eth1'])
                conn.sendall(return_value)
        except socket.error as error:
            print 'Error while receiving data from host: {error}'.format(error=error)

except socket.gaierror as error:
    print 'Address-related error while accepting connections from client!: {error}'.format(error=error)