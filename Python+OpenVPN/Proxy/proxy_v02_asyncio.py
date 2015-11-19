__author__ = 'Elias Eckenfellner'
import argparse
import sys
import asyncio
import signal
import socket

#Ob Proxy auf der Server- oder Client-Seite läuft
SERVER=False
#Gegenüber
PEER_IP="10.0.0.2"
#Eigene externe IP
EXT_IP="10.0.0.1"

##########
#Statisch#
##########
#Externer Port beider Seiten
PORTEXT=6222
#Interne IP und Port(Localhost)
INT=("127.0.0.1", 6221)
#Interne IP und Port des VPN-Servers/Clients(Localhost)  --- Port bei Client unbekannt
LOCALVPN=("127.0.0.1", 6220)

PEER=(PEER_IP, PORTEXT)
EXT=(EXT_IP, PORTEXT)

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
class INTERN:
  def connection_made(self, transport):
      self.transport = transport

  def datagram_received(self, data, addr):
      global ext
      global SERVER
      global localvpnport

      print("int to ext")
      if(SERVER is False and localvpnport is not 0):
          localvpnport=addr[1]
       #Am Outside-Sockel senden
      ext.sendto(data, PEER)

  def error_received(self, exc):
      print('Error received:', exc)

  def connection_lost(self, exc):
      print('stop', exc)


#Aussen empfangen und innen senden
class EXTERN:
  def connection_made(self, transport):
      self.transport = transport

  def datagram_received(self, data, addr):
      global int
      global SERVER
      global localvpnport
      print("ext to int")
      #Am Inside-Sockel senden
      if(SERVER is False):
          int.sendto(data, ("127.0.0.1", localvpnport))
      else:
          int.sendto(data, LOCALVPN)

  def error_received(self, exc):
      print('Error received:', exc)

  def connection_lost(self, exc):
      print('closing transport', exc)


def start_intern(loop, addr):
  t = asyncio.Task(loop.create_datagram_endpoint(
      INTERN, local_addr=addr))
  transport, server = loop.run_until_complete(t)


def start_extern(loop, addr):
  t = asyncio.Task(loop.create_datagram_endpoint(
      EXTERN, remote_addr=addr))
  loop.run_until_complete(t)

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  intern_obj = start_intern(loop, INT)
  extern_obj = start_extern(loop, EXT)
  loop.run_forever()
  intern_obj.close()
  extern_obj.close()
  loop.close()