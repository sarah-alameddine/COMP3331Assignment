import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 2129))



username = input("Enter Username:")
s.send(username.encode())

# print from server "enter password 
msg = s.recv(1024).decode()
print(msg)

password = input()
s.send(password.encode())

msg = s.recv(1024).decode()
print(msg)


'''
while msg.lower().strip() != 'logout':
	s.send(msg.encode())
	#s.sendto(message.encode(),(serverName, serverPort))
		#msg = 
	msg = input("Enter mesg:")

'''

