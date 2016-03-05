__author__ = 'Elias Eckenfellner'

import socket, sys, threading, asyncio

SERVER=True
PEER=("10.0.0.2", 6222)
LOCALVPN=("localhost", 6220)

EXT=("10.0.0.1", 6222)
INT=("localhost", 6221)

#Immer 0
localvpnport=0

#socket_int_rec2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket_int_rec2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#socket_int_rec2.bind(INT)

#except:
    #print ("Could not set up EXT socket.")
    #sys.exit(1)


#Socket um bei "int to ext" ext zu senden
ext=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ext.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ext.bind(EXT)

#Socket um bei "ext to int" int zu senden
int=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
int.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
int.bind(INT)

#Vom Programm benötigte globale Variable
localvpnport=0

#Innen empfangen und nach aussen senden
class Intern:
  def connection_made(self, transport):
      self.transport = transport

  def datagram_received(self, data, addr):
      global ext
      global SERVER
      global localvpnport

      print("int to ext")
      if(SERVER is False and localvpnport is not 0):
          localvpnport=addr[1]
      #Am Outside-Sockel sende
      try:
        ext.sendto(data, PEER)
      except:
          pass


  def error_received(self, exc):
      print('Error received:', exc)

  def connection_lost(self, exc):
      print('stop', exc)


#Aussen empfangen und innen senden
class Extern:
  def connection_made(self, transport):
      self.transport = transport

  def datagram_received(self, data, addr):
      global int
      global SERVER
      global localvpnport
      print("ext to int")
      #Am Inside-Sockel senden
      if(SERVER is False):
          try:
            int.sendto(data, ("127.0.0.1", localvpnport))
          except:
              pass
      else:
          try:
            int.sendto(data, LOCALVPN)
          except:
              pass

  def error_received(self, exc):
      print('Error received:', exc)

  def connection_lost(self, exc):
      print('closing transport', exc)


def start_intern(loop, addr):
  t = asyncio.Task(loop.create_datagram_endpoint(
      Intern, local_addr=addr))
  transport, server = loop.run_until_complete(t)


def start_extern(loop, addr):
  t = asyncio.Task(loop.create_datagram_endpoint(
      Extern, remote_addr=addr))
  loop.run_until_complete(t)

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  intern_obj = start_intern(loop, INT)
  extern_obj = start_extern(loop, EXT)
  loop.run_forever()
  intern_obj.close()
  extern_obj.close()
  loop.close()
