import json
import os, sys, time

def send_to(message):

    try:
        print("writing: ", message)
        os.write(4, bytes(f'{message}\n',"UTF-8")) #4
    except Exception as err:
        time.sleep(10)


while True:

    try:
        pw = os.open("pipeFrom", os.O_WRONLY) #pipe client - > server
        pr = os.open("pipeTo", os.O_RDONLY | os.O_CREAT) #pipe server - > client
        rf = os.fdopen(pr, 'rb', 0)
        
        req = rf.read()
        feedback = "Response on message from client at {0} data: {1}".format(time.time(),req)
        
        print('Request from client: ', req)

        if bool(req):
            writesBytes = os.write(pw, bytes(feedback,"utf-8"))
            
        rf.close()
        time.sleep(5)

    except KeyboardInterrupt:   
        rf.close()
        print("Child closing")
        sys.exit(0)