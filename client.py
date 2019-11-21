import socket
import time
import sys
from threading import Timer
flag = True

def timeout_client():
    print('No input detected - Connection has been closed by server')
    sys.exit(0)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 29025))

    while True:
        msg_recieved = s.recv(1024).decode()
        print(msg_recieved)

        if str(msg_recieved) == "<BREAK>":
            msg_recieved = ''
            print("Connection has been closed by server")
            sys.exit(0)

        # Implements a timeout so if a user isnt active after a period of time logs them out
        timeout = 60
        # if t is cancelled then call the timeout_client function
        t = Timer(timeout, timeout_client,)
        t.start()
        prompt = "You have %d seconds to type else you will be disconnected from server\n" % timeout

        msg_sent = input(prompt)
        t.cancel()
        s.send(msg_sent.encode())

    sys.exit(0)





#     import socket
# import time
# import sys
# from threading import Timer
# flag = False


# class AdventureDone(Exception): pass

# def timeout_client():
#     print('No input detected - Connection has been closed by server')
#     raise AdventureDone

# if __name__ == "__main__":
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((socket.gethostname(), 29025))
#     try:
#         while True:
#             msg_recieved = s.recv(1024).decode()
#             print(msg_recieved)

#             if str(msg_recieved) == "<BREAK>":
#                 msg_recieved = ''
#                 print("Connection has been closed by server")
#                 sys.exit(0)

#             # Implements a timeout so if a user isnt active after a period of time logs them out
#             timeout = 5
#             # if t is cancelled then call the timeout_client function
#             t = Timer(timeout, timeout_client,)
#             t.start()
#             prompt = "You have %d seconds to type else you will be disconnected from server\n" % timeout

#             msg_sent = input(prompt)
#             t.cancel()
#             s.send(msg_sent.encode())

#     except AdventureDone:
#         break
#     s.close()