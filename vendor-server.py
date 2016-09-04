import socket
import threading
import json
import sqlite3

bind_ip = ''
bind_port = 2000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] Listening on %s:%d" % (bind_ip, bind_port))

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("===Received\n%s" % request) # bytes
    url = str(request).split()[1].split('/')
    url.pop(0)

    print("===url[0]: %s" % url[0])
    if url[0] == '':
        print("===Menu")
        cursor = sqlite3.connect("test.db").cursor()
        cursor.execute("select * from menu")
        data = { "itemList": [ { 'name':  row[0], 'price': row[1], 'value': row[2] } for row in cursor.fetchall()] }
        client_socket.send(json.dumps(data).encode())
    elif url[0] == 'buy':
        print("===Buy")
        pass
    elif url[0] == 'images':
        print("===Images")
        print("===Send %s" % url[1])
        client_socket.send(open('./images/%s' % url[1], "rb").read())

    client_socket.close()

while True:
    client,addr = server.accept()
    print("\n===[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    client_handler = threading.Thread(target=handle_client, args=(client, ))
    client_handler.start()
