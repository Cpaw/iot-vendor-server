import socket
import json
import sqlite3

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("===Received\n%s" % request) # bytes
    url = str(request).split()[1].split('/')
    url.pop(0)

    print("===url[0]: %s" % url[0])
    if url[0] == '':
        print("===Menu")
        cursor.execute("select * from menu")
        data = {"itemList": [{'name': row[0], 'price': row[1], 'value': row[2]} for row in cursor.fetchall()]}
        client_socket.send(json.dumps(data).encode())
    elif url[0] == 'buy':
        # TODO 0 valid
        print('===Buy '  + url[1])
        cursor.execute('update menu set value=value-1 where name=?', (url[1],))
        client_socket.send(('Buy ' + url[1]).encode())
    elif url[0] == 'max':
        print('===Max '  + url[1])
        cursor.execute('update menu set value=4 where name=?', (url[1],))
        client_socket.send(('Max ' + url[1]).encode())
    elif url[0] == 'images':
        print("===Images")
        print("===Send %s" % url[1])
        client_socket.send(open('./images/%s.jpg' % url[1], "rb").read())
    elif url[0] == 'stop':
        global gLoopStatus
        gLoopStatus = False


bind_ip = ''
bind_port = 2000
gLoopStatus = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] Listening on %s:%d" % (bind_ip, bind_port))

connect = sqlite3.connect("test.db")
cursor = connect.cursor()

while gLoopStatus:
    client, addr = server.accept()
    print("\n===[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    handle_client(client)
    client.close()

cursor.close()
connect.close()
server.close()
