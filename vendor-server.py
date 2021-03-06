import socket
import json
import os
import sqlite3

def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]

def record_is_exist(name):
    cursor.execute('select count(*) from menu where name=?', (name,))
    return True if 0 != cursor.fetchone()[0] else False

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
        cursor.execute('update menu set value=3 where name=?', (url[1],))
        client_socket.send(('Max ' + url[1]).encode())
    elif url[0] == 'images':
        print('===Images')
        name = get_basename(url[1]) # 一旦拡張子を消す(最初からなくてもOK)
        if not record_is_exist(name):
            name = 'notfound'
        print('===Send image ' + name)
        client_socket.send(open('./images/%s.jpg' % name, 'rb').read())
    elif url[0] == 'stop':
        return False
    return True


bind_ip = ''
bind_port = 2000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] Listening on %s:%d" % (bind_ip, bind_port))

connect = sqlite3.connect('./jihanki.db')
cursor = connect.cursor()

loop_state = True
while loop_state:
    client, addr = server.accept()
    print("\n===[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    loop_state = handle_client(client)
    client.close()

cursor.close()
connect.commit()
connect.close()
server.close()
