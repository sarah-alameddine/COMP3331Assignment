import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 22288))

while True:
    msg = s.recv(1024).decode()
    print(msg)
    message = input()
    s.send(message.encode())

# while True:
#     message = input()
#     s.send(message.encode())

    # # print from server "enter password 
    # msg = s.recv(1024).decode()
    # print(msg)

    # password = input()
    # s.send(password.encode())

    # msg = s.recv(1024).decode()
    # print(msg)

    # If message is not empty - send it
    # if message:
    #     s.send(message.encode())

    # try:
    #     # Now we want to loop over received messages (there might be more than one) and print them
    #     while True:
    #         message = client_socket.recv(1024).decode()
    #         # Print message
    #         print("%" % (message)
