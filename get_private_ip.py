__author__ = 'Alexander Mark, FireVPN'
# uses Python 3.4 Interpreter, netifaces (with yum/dnf python-devel.x86_64 packet)
import socket
import netifaces

from netifaces import interfaces, ifaddresses, AF_INET
def get_private_ip():
    ifaces=dict()
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        ifaces[ifaceName]= addresses
    return ifaces

