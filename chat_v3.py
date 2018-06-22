import socket
import threading
import os
import time

def clear_scr():
	os.system("cls")

HOST, PORT = "", 1337

MSG_LEN_BYTES = 4
ENCODING = "utf-8"

recieved = []

clients = []

class Client:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = int(port)
	
	def connect(self):
		try:
			with socket.create_connection((self.ip, self.port), timeout=1) as self.socket:
				msg = b"|ping|"
				ln = (len(msg)).to_bytes(MSG_LEN_BYTES, 'big')
				self.socket.sendall(ln+msg)
		except Exception as e:
			print(f"Exception while connecting to {self.ip} {self.port}")
			print(e)
	
	def send(self, msg_s):
		try:
			with socket.create_connection((self.ip, self.port), timeout=1) as self.socket:
				msg = msg_s.encode(ENCODING)
				ln = (len(msg)).to_bytes(MSG_LEN_BYTES, 'big')
				self.socket.sendall(ln+msg)
		except Exception as e:
			print(f"Exception while connecting to {self.ip} {self.port}")
			print(e)
		
			
		
		

"""
def connected_thread(sock, addr):
	global recieved
	while True:
		sock.settimeout(60)
		ln = sock.recv(MSG_LEN_BYTES)
		msg = sock.recv(int.from_bytes(ln, 'big'))
		recieved.append(f"{addr}: {msg.decode(ENCODING)}")
"""
def server_thread(host, port):
	with socket.socket() as sock:
		sock.bind((host, port))
		sock.listen(20)
		while True:
			s, addr = sock.accept()
			
			try:
				s.settimeout(1)
				ln = s.recv(MSG_LEN_BYTES)
				msg = s.recv(int.from_bytes(ln, 'big'))
				s.close()
				recieved.append(f"{addr}: {msg.decode(ENCODING)}")
			except Exception as e:
				print(e)
				time.sleep(1)
		#thr = threading.Thread(target=connected_thread, args=(s, addr))
		#thr.daemon = True
		#thr.start()

thr = threading.Thread(target=server_thread, args=(HOST, PORT))
thr.daemon = True
thr.start()

print("Server started")

with open("clients.txt", "r") as f:
	for line in f:
		clients.append(Client(*line.split()))

input("Press ENTER to connect")

for client in clients:
	client.connect()

time.sleep(1)

print("Done")

while True:
	inp = input()
	if inp != "":
		recieved.append(f"SELF: {inp}")
		for client in clients:
			client.send(inp)
	clear_scr()
	for msg in recieved:
		print(msg)
