import os
from socket import *
import random

IPAddress = '127.0.0.1'
port = 2121
info = (IPAddress, port)
BUFFERSIZE = 2048
response = ''

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(info)




serverSocket.listen()
connectionSocket, retAddr = serverSocket.accept()

rootPath = os.getcwd()


def pwd():
    currentAbsolutePath = os.getcwd();
    currentRelativePath = currentAbsolutePath.replace(rootPath,'')
    print(currentRelativePath)
    if not currentRelativePath :
        currentRelativePath = '\\'
    return currentRelativePath

def changeDirectory(path):
    response = ''
    if path =='\\'or path =='/':
        os.chdir(rootPath)
        response = 'Directory changed to root path :  \\';
    elif not os.path.exists(path):
        response ='The system cannot find the path specified.'
        print(response)
    elif os.path.isdir(path):
        pathBeforeChange = os.getcwd()
        os.chdir(path)
        if not rootPath in os.getcwd():
            os.chdir(pathBeforeChange)
            response = "Access Denied..."
        else :
            currentRelativePath = os.getcwd().replace(rootPath , '')
            if not currentRelativePath : currentRelativePath = '\\'
            print('Directory changed to ' + os.getcwd())
            response = 'Directory changed to ' + currentRelativePath;
    return response

def list():
    list_files = os.listdir()
    size_files = 0
    ans = '\n' + f'{"file name":<{20}}size of file' +'\n\n'
    
    for file in list_files:
        size_files += os.path.getsize(file)
        if os.path.isdir(file):
            ans += '>'  + f'{file:<{20}}' + (str(os.path.getsize(file))) + '  bytes' + '\n'
        if os.path.isfile(file):
            ans += f'{file:<{21}}' + (str(os.path.getsize(file))) + '  bytes'  + '\n'

    ans +=  f'{"size of files":<{21}}' + (str(size_files)) + '  bytes'  +'\n\n'

    return ans


def dwld(file):
    files = os.listdir()
    if file in files:
        dwld_port = random.randint(3000 , 50000)
        dwld_server = socket(AF_INET, SOCK_STREAM)
        dwld_server.bind((IPAddress , dwld_port))
        dwld_server.listen()
        connectionSocket.send(str(dwld_port).encode())
        dwld_con , addr = dwld_server.accept()
        with open(file , 'rb') as file:
            data = file.read()
            dwld_con.send(data)
            dwld_con.close()
        return 'Download complete successfull'
    else:
        connectionSocket.send('the file is not in this folder'.encode())
        return 'the file is not in this folder'


while True:
    print("Wiating for clients...")
    requestMessage = connectionSocket.recv(BUFFERSIZE).decode()
    
    
    if requestMessage.lower() == 'pwd':
        response = pwd()
    
    elif requestMessage.lower() == 'list':
        response = list()

    elif requestMessage.startswith('cd'):
        response = changeDirectory(requestMessage[3:])

    elif requestMessage.startswith('dwld'):
        response = dwld(requestMessage[5:])

     
    print(response)
            
    connectionSocket.send(response.encode())