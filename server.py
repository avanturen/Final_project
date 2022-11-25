import socketserver
import config
import json
from game_classes import *

class MyTCPHandler(socketserver.BaseRequestHandler):
	characters = []

	def search_by_name(self, name):
		for i in range(len(self.characters)):
			if self.characters[i]['name'] == name:
				return i
		return -1
	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		data = json.loads(self.data.decode('utf8'))
		index = self.search_by_name(data['name'])
		print("ok")
		if index != -1:
			self.characters[index] = data
		else:
			self.characters.append(data)
		self.request.send(json.dumps(self.characters).encode('utf8'))
# just send back the same data, but upper-cased
        

def start_server(HOST = config.HOST, PORT = config.PORT):
	 # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


if __name__ == "__main__":
    start_server()