import socket
import threading
import os
import time

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

def update_text():
	global app
	app.update_text()

def clear_scr():
	os.system("cls")

HOST, PORT = "", 1337

MSG_LEN_BYTES = 4
ENCODING = "utf-8"

recieved = []
to_send = []
clients = []

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.create_widgets()
		self.ls = 0
		

	def send(self, event):
		msg = self.msg.get()
		self.msg.set("")
		to_send.append(msg)
		recieved.append(f"SELF: {msg}")
		self.update_text()
	
	def update_text(self):
		global recieved
		self.text_show.delete(1.0, 'end')
		self.text_show.insert('end', "\n".join(recieved))
	
	def create_widgets(self):
		self.text_show = ScrolledText(self)
		
		self.text_show.pack()
		
		
		self.text_show["takefocus"] = 0
		
		self.msg = tk.StringVar()
		
		self.prompt = tk.Entry(self)
		
		self.prompt["textvariable"] = self.msg
		
		self.prompt.pack(fill="x")
		
		self.prompt.bind('<Key-Return>', self.send)
		
		self.quit = tk.Button(self, text="QUIT", fg="red",
							  command=root.destroy)
		self.quit.pack(side="bottom", fill="x")

class Client:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = int(port)
		self.queue = []
	
	"""	
	def connect(self):
		try:
			with socket.create_connection((self.ip, self.port), timeout=1) as self.socket:
				msg = b"|ping|"
				ln = (len(msg)).to_bytes(MSG_LEN_BYTES, 'big')
				self.socket.sendall(ln+msg)
		except Exception as e:
			print(f"Exception while connecting to {self.ip} {self.port}")
			print(e)
	"""
	
	def send(self, msg_s):
		self.queue.append(msg_s)
		
		for i in range(5):
			if len(self.queue) == 0:
				break
			
			msg = self.queue.pop()
			
			if self.send_lite(msg):
				pass
			else:
				self.queue.append(msg)
				break
			
	
	def send_lite(self, msg_s):
		
		
		try:
			with socket.create_connection((self.ip, self.port), timeout=0.1) as self.socket:
				msg = msg_s.encode(ENCODING)
				ln = (len(msg)).to_bytes(MSG_LEN_BYTES, 'big')
				self.socket.sendall(ln+msg)
		except Exception as e:
			print(f"Exception while connecting to {self.ip} {self.port}")
			print(e)
			return False
		return True
		
			
		
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
				print(recieved[-1])
				update_text()
			except Exception as e:
				print(e)

def network_thread(to_send, clients):
	while True:
		time.sleep(0.2)
		while len(to_send) > 0:
			msg = to_send.pop()
			for client in clients:
				client.send(msg)


thr = threading.Thread(target=server_thread, args=(HOST, PORT))
thr.daemon = True
thr.start()

thr = threading.Thread(target=network_thread, args=(to_send, clients))
thr.daemon = True
thr.start()


print("Server started")

with open("clients.txt", "r") as f:
	for line in f:
		clients.append(Client(*line.split()))

#input("Press ENTER to connect")

#for client in clients:
#	client.connect()

#time.sleep(1)

#print("Done")

"""
while True:
	inp = input()
	if inp != "":
		recieved.append(f"SELF: {inp}")
		for client in clients:
			client.send(inp)
	clear_scr()
	for msg in recieved:
		print(msg)
"""

root = tk.Tk()
app = Application(master=root)
app.mainloop()
