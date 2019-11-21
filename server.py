import socket
#from _thread import *
from threading import Thread
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 27645))
#t_lock=threading.Condition()

def set_up_clients():
	while True:
		client_socket, client_address = server.accept()
		print("New connection: %s : %s!" % client_address)
		client_socket.send(str.encode('Please enter username'))
		Thread(target=run, args=(client_socket, client_address,)).start()

def run(client_socket, client_address):
	global username_socket
	#global t_lock
    # global client_Socket
    # global server_Socket
	loginUser(client_socket, client_address)

	while True:
		 #get lock as we might me accessing some shared data structures
		#with t_lock:
		userInput = client_socket.recv(1024).decode()
		dataList = str(userInput).split(" ",2)
		print(dataList[0])

		if str(userInput) == "logout":
			presence_logout(client_socket, client_address)
			error = "<BREAK>"
			client_socket.send(error.encode())
			break

		######### whoelse ####################
		if dataList[0] == "whoelse":
			print(username_socket)
			data = ("TESTING WHOELSE")
			client_socket.send(data.encode())
			continue

		######### whoelsesince ###############
		elif dataList[0] == "broadcast":	
			data = ("TESTING broadcast")
			client_socket.send(data.encode())
			continue

		############ MESSEGE #################
		elif dataList[0] == "message":
			data = ("TESTING message")
			client_socket.send(data.encode())
			continue

		######### whoelse ####################
		elif dataList[0] == "broadcast":
			data = ("TESTING broadcast")
			client_socket.send(data.encode())
			continue

		######### BLOCK ####################
		elif dataList[0] == "block":
			data = ("TESTING block")
			client_socket.send(data.encode())
			continue

		######### UNBLOCK ####################
		elif dataList[0] == "unblock":
			data = ("TESTING unblock")
			client_socket.send(data.encode())
			continue

		######## INVALID COMMAND ########
		else:
			data = ("Error. Invalid command")
			client_socket.send(data.encode())
			continue

			#notify other thread
			#t_lock.notify()
		#sleep for UPDATE_INTERVAL
		#time.sleep(UPDATE_INTERVAL)

# Notifies all users when a new user connects
def presence_login(client_socket, userInput):
	global online

	online.append(client_socket)
	for x in online:
		print(x)
		data = ("\nNEW USER LOGGED IN - %s" % str(userInput))
		x.send(data.encode())

def presence_logout(client_socket, userInput):
	global online

	for i in online :
		if client_socket == i:
			online.remove(i)
			break

	for x in online:
		print(x)
		data = ("\n User %s has logged out" % str(userInput))
		x.send(data.encode())

	# for socket in clients:
	# 	if (socket != client_socket):
	# 		send_to_all = "\nNEW USER LOGGED IN - %s" % clients[socket]
	# 		socket.send(send_to_all.encode())

	# Go through dictionary of all online clients and notify then when new user logs in
	# for socket in clients_online:
	# 	send_to_all = "\n NEW USER LOGGED IN - %s" % clients_online[socket]
	# 	socket.send(send_to_all.encode())



def loginUser(client_socket, client_address):
	passwordTries = 2
	global username_socket
	
	while True:
		userInput = client_socket.recv(1024).decode()
		start = time.time()
		
		#if no messages by client 
		if not userInput:
			print("NO USER INPUT DETECTED")
			end = time.time()
			if (end - start ) > 10:
				error = "<BREAK>"
				client_socket.send(error.encode())

		############ CHECK IF USER BLOCKED FOR UNSECC ATTEMPTS #################
		# If a user is in the failed_attemp dictionary and
		# if they have not waited 60 seconds return
		if str(userInput) in client_failed_attemp:
			end = time.time()
			result = end - client_failed_attemp[str(userInput)]
			if result < 60:
				data = "Your account is blocked due to multiple login failures. Please try again later"
				client_socket.send(data.encode())
				error = "<BREAK>"
				client_socket.send(error.encode())
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
			client_socket.send(data.encode())
			passInput = client_socket.recv(1024).decode()
			# If the user has entered the correct password -  LOGIN SUCCESSFUL
			if userDict[str(userInput)] == str(passInput):
				data = "LOGIN SUCCESSFUL"
				client_socket.send(data.encode())
				##############################################
				# PRESENCE NOTIF: Add them to the list of online and notify others of presence
				presence_login(client_socket, str(userInput))
				username_socket[str(userInput)] = client_socket
				break # LOGIN SUCCESS!

			# If password entered is wrong - LOGIN UNSUCCESSFUL
			else:
				while passwordTries != 0:
					data = ("Invalid Password. Please try again")
					client_socket.send(data.encode())
					passInput = client_socket.recv(1024).decode()
					if userDict[str(userInput)] == str(passInput):
						data = "LOGIN SUCCESSFUL"
						client_socket.send(data.encode())
						##############################################
						# PRESENCE NOTIF: Add them to the list of online and notify others of presence
						presence_login(client_socket, str(userInput))
						username_socket[str(userInput)] = client_socket
						break # LOGIN SUCCESS!
					else:
						passwordTries = passwordTries - 1

			# If they used up all their attemps shut terminal down
			if passwordTries == 0:
				data = ("Your account is blocked due to multiple login failures. Please try again later")
				client_socket.send(data.encode())
				# Record the user and begin timer
				start = time.time()
				client_failed_attemp[str(userInput)] = start
				error = "<BREAK>"
				client_socket.send(error.encode())
		# else if username not correct
		else:
			askUserAgain = "Please enter valid Username:"
			client_socket.send(askUserAgain.encode())
			continue
			#userInput = client_socket.recv(1024).decode()

	print("EVERYTHING IS WORKING SO FARR")
	return

		
######################## MAIN #################################


# Stores all the usernames & passwords 
userDict = {}
client_failed_attemp = {}
online = []


clients_online = {}
username_socket = {}

# Open the credential.txt file to store usernames and passwords in dictionary
# Stores the left column as users (keys) and the right colum as passwords(value)
with open("Credentials.txt") as credFile:
    for line in credFile:
       (key, val) = line.split()
       userDict[key] = val

# Set up a dictionary that will contain key(username) : values[conn,addr,online]
# At the start values will be none,none, false
for user in userDict:
	clients_online.setdefault(user, [])

if __name__ == "__main__":
	server.listen(5) 
	print ("Server is up and running - Waiting for connections from TCP clients!")
	#send_thread = threading.Thread(name="RecvHandler",target=set_up_clients)
	send_thread = Thread(target=set_up_clients)
	send_thread.start()
	send_thread.join()
	server.close()


