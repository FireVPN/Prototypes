__author__ = 'Alexander Mark, FireVPN'
# uses Python 3.4 Interpreter, ipgetter
# uses DNS to resolve name (my-ip-address.net), Data from this server is send via Port 80 (HTTP)

import ipgetter
def get_public_ip():
    import ipgetter
    IP = ipgetter.myip()
    return IP

