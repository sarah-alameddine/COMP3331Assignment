import socket
#from _thread import *
from threading import Thread
import time

userDict = {} # Stores all the usernames & passwords 
# A header will store the length of the messeges sent

client_failed_attemp = {}


# i = 40
# start = time.time()
# print(start)
# time.sleep(60)

# end = time.time()
# print(end)
# print(end - start)

def run():

	while True:
		#TODO ADD TO THE LIST OF CLIENT
		#clientsocket.send(str.encode('Please enter username'))
		#userInput = clientsocket.recv(1024).decode()
		clientsocket, address = s.accept()

		###################
        #client, client_address = SERVER.accept()
		print("%s:%s has connected." % address)
		clientsocket.send(str.encode('Please enter username'))
		addresses[clientsocket] = address
		Thread(target=loginUser, args=(clientsocket, address,)).start()

def presence():

def loginUser(clientsocket, address ):
	# clientsocket, address = s.accept()
	# clientsocket.send(str.encode('Please enter username'))
	# userInput = clientsocket.recv(1024).decode()

	passwordTries = 2

	while True:
		userInput = clientsocket.recv(1024).decode()
		start = time.time()
		
		#if no messages by client 
		if not userInput:
			print("NO USER INPUT DETECTED")
			end = time.time()
			if (end - start ) > 10:
				error = "<BREAK>"
				clientsocket.send(error.encode())

		############ CHECK IF USER BLOCKED FOR UNSECC ATTEMPTS #################
		# If a user is in the failed_attemp dictionary and
		# if they have not waited 60 seconds return
		if str(userInput) in client_failed_attemp:
			end = time.time()
			result = end - client_failed_attemp[str(userInput)]
			if result < 60:
				data = "Your account is blocked due to multiple login failures. Please try again later"
				clientsocket.send(data.encode())
				error = "<BREAK>"
				clientsocket.send(error.encode())
			# Else remove them from list and continue
			else :
				client_failed_attemp.pop(str(userInput))
		
		############ CHECK IF USER NAME EXITS #############################
		# Search if the username the user entered exist
		if str(userInput) in userDict:
			print("user exist")
			user = userInput

			# if it exist ask for password
			data = "Enter password:"
			clientsocket.send(data.encode())
			passInput = clientsocket.recv(1024).decode()
			# If the user has entered the correct password -  LOGIN SUCCESSFUL
			if userDict[str(userInput)] == str(passInput):
				data = "LOGIN SUCCESSFUL"
				clientsocket.send(data.encode())
				break # LOGIN SUCCESS!

			# If password entered is wrong - LOGIN UNSUCCESSFUL
			else:
				while passwordTries != 0:
					data = ("Invalid Password. Please try again")
					clientsocket.send(data.encode())
					passInput = clientsocket.recv(1024).decode()
					if userDict[str(userInput)] == str(passInput):
						data = "LOGIN SUCCESSFUL"
						clientsocket.send(data.encode())
						break
					else:
						passwordTries = passwordTries - 1

			# If they used up all their attemps shut terminal down
			if passwordTries == 0:
				data = ("Your account is blocked due to multiple login failures. Please try again later")
				clientsocket.send(data.encode())
				# Record the user and begin timer
				start = time.time()
				client_failed_attemp[str(userInput)] = start
				error = "<BREAK>"
				clientsocket.send(error.encode())
		# else if username not correct
		else:
			askUserAgain = "Please enter valid Username:"
			clientsocket.send(askUserAgain.encode())
			continue
			#userInput = clientsocket.recv(1024).decode()

	print("EVERYTHING IS WORKING SO FARR")

		
######################## MAIN #################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 29025))
#s.listen(5)
threads = []
clients = {}
addresses = {}
# Open the credential.txt file to store usernames and passwords in dictionary
# Stores the left column as users (keys) and the right colum as passwords(value)
with open("Credentials.txt") as credFile:
    for line in credFile:
       (key, val) = line.split()
       userDict[key] = val

if __name__ == "__main__":
	s.listen(4) 
	print ("Multithreaded Python server : Waiting for connections from TCP clients...")
	ACCEPT_THREAD = Thread(target=run)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	s.close()
# 	(conn, (ip,port)) = s.accept() 
# 	newthread = run() 
# 	newthread.start() 
# 	threads.append(newthread) 
 
# for t in threads: 
#     t.join() 

