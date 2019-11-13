import socket


# A header will store the length of the messeges sent

# userDict
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

username = {
	"sarah": "123"
}

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established")
    
    print(f"Enter Username:")
    
    # msg = s.recv(10)
     
     clientsocket.recv(10)
