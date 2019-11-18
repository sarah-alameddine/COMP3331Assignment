import socket


userDict = {} # Stores all the usernames & passwords 
# A header will store the length of the messeges sent


def loginUser():
	clientsocket, address = s.accept()
	print(f"connection from {address} has been established")

	userInput = clientsocket.recv(1024).decode()

	while True:
		# Search if the username the user entered exist
		if str(userInput) in userDict:
			print("user exist") 
			break
		else:
			askUserAgain = "Please enter valid Username:"
			clientsocket.send(askUserAgain.encode())
			userInput = clientsocket.recv(1024).decode()
			
	# If user enters a valid username - ask for password
	if userLoginSucc == True:
		data = "ENter password"
		clientsocket.send(data.encode())
		
	# If user enters a valid username - ask for password
	passInput = clientsocket.recv(1024).decode()

	# if the user has entered the correct password - login success
	if userDict[str(userInput)] == str(passInput):
		data = "LOGIN SUCCESSFUL"
		clientsocket.send(data.encode())
		
		
		
######################## MAIN #################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 2129))
s.listen(5)

# Open the credential.txt file to store usernames and passwords in dictionary
# Stores the left column as users (keys) and the right colum as passwords(value)
with open("Credentials.txt") as credFile:
    for line in credFile:
       (key, val) = line.split()
       userDict[key] = val

loginUser()

	
