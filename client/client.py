from socket import *
import os

serverIPAddress = "127.0.0.1"
serverPort = 2121
serverInfo = (serverIPAddress, serverPort)
BUFFERSIZE = 2048

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverInfo)

finalReq = ''

def help():
    commandsLsit = {
        'HELP': "Help you to write any command",
        'LIST': "Show all the files in the current directory",
        'DWLD': "Download file",
        'PWD': "Show the current directory",
        "CD": "Change directory",
        "QUIT": "Exit"
    }
    print()
    for command, helpText in commandsLsit.items():
        print(command, " : ", helpText)


def dwld(command):
    clientSocket.send(command.encode())
    dwld_port = clientSocket.recv(BUFFERSIZE).decode()
    if not dwld_port == 'the file is not in this folder':
        dwld_connection = socket(AF_INET, SOCK_STREAM)
        dwld_connection.connect((serverIPAddress , int(dwld_port)))
        data = b''
        while True:
            section = dwld_connection.recv(BUFFERSIZE)
            data += section
            if not section:
                break
        with open(command[5:]
 , 'wb') as file:
            file.write(data)
            dwld_connection.close()

def sendRquest(reqMessage):
    clientSocket.send(reqMessage.encode())
    response = clientSocket.recv(BUFFERSIZE).decode()
    print(response) 
   
help()
 
while True:
    userCommand = input('Type your command to get response ...   ')
    
    if  userCommand.startswith('cd') \
        or userCommand.startswith('pwd') \
        or userCommand.startswith('list') :
            finalReq = userCommand
            sendRquest(finalReq)
       
    elif userCommand == 'help':
        help()

    elif userCommand.startswith('dwld'):
        dwld(userCommand)
        response = clientSocket.recv(BUFFERSIZE).decode()
        print(response)   
             
    else :
        print(f'Command "{userCommand}" Not Found ... ')