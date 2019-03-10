import django
import os
import sys
import socket

sys.path.append("/Users/ishar/Desktop/diso/Diso/diso/website")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from accounts.models import Table

# my server setup to allow the pi to communicate
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '192.168.3.98'
port = 50000
address = (ip, port)
server.bind(address)
server.listen(1)
print('Listening on MI5 servers ' + str(address))
conn, addr = server.accept()
print('Connected to 007: ' + str(addr[0]) + ': ' + str(addr[1]))

while 1:
    data = conn.recv(1024)
    data_string = str(data)
    # print(data_string)
    # b'1' is the code for occupied
    if data_string == "b'1'":
        # sets the table to un-available (each pi will be assigned to one table, in this case id 5)
        table = Table.objects.get(id=5)
        table.available = False
        table.save()
        print('occupied')

    else:
        # sets the table to un-available (each pi will be assigned to one table, in this case id 5)
        table = Table.objects.get(id=5)
        table.available = True
        table.save()
        print('available')

    conn.sendall(data)

