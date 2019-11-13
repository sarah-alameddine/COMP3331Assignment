import socket

# Dictionary will store all the usernames & passwords 
userDict = {}
# A header will store the length of the messeges sent


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 2495))
s.listen(5)


# Open the credential.txt file to store usernames and passwords in dictionary
# Stores the left column as users (keys) and the right colum as passwords(value)
with open("Credentials.txt") as f:
    for line in f:
       (key, val) = line.split()
       userDict[key] = val


# now our endpoint knows about the OTHER endpoint.
clientsocket, address = s.accept()
print(f"connection from {address} has been established")


userInput = clientsocket.recv(1024).decode()

if str(userInput) in userDict:
	print("userexist") 
	data = "ENter password"
	clientsocket.send(data.encode())
	
passInput = clientsocket.recv(1024).decode()

# if the user has entered the correct password - login success
if userDict[str(userInput)] == str(passInput):
	data = "LOGIN SUCCESSFUL"
	clientsocket.send(data.encode())

	
