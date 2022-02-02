import socket

ROBOT_ADDR = '172.16.7.103' #
MPU9150_PORT = 44444

class UDP_Send(): 
   def __init__(self,addr,port):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK.DGRAMとすることで、UDPを指定
      self.addr = addr
      self.port = port

   def send(self,list):
      self.sock.sendto(list,(self.addr,self.port))
      return 0

class UDP_Recv(): 
   def __init__(self,addr,port):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.sock.bind((addr,port))
      self.sock.setblocking(0)

   def recv(self):
      message,address = self.sock.recvfrom(400000)

      return message
