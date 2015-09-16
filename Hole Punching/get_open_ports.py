__author__ = 'Alexander Mark, FireVPN'
# uses Python 3.4 Interpreter

import socket
import subprocess
import sys
from datetime import datetime
import ipgetter


def portscan():
# use own public IP to scan (testing)
    ip= ipgetter.myip()
    remoteServerIP  = ip

#open ports found
    open_ports=list()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors

    try:
        for port in range(1,1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                open_ports=open_ports.append(port)
            sock.close()

    except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    except socket.error:
        print "Couldn't connect to server"
        sys.exit()

    return open_ports