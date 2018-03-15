Forward TCP traffic (**port forward**) from local port to an other TCP socket server and display transfered data

```python
#!/usr/bin/python3
import socket
import sys
import _thread 
import time

def server(c):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind((c[0], c[1]))
        dock_socket.listen(16)
        while True:
            client_socket = dock_socket.accept()[0]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((c[2], c[3]))
            _thread.start_new_thread(forwarder, (client_socket, server_socket, True))
            _thread.start_new_thread(forwarder, (server_socket, client_socket, False))
    except:
        pass

def forwarder(source, destination, direction):
    data = True
    while data:
        data = source.recv(1024)
        if data:
            destination.sendall(data)
            print(">"*80) if direction else print("<"*80)
            print(data)
        else:
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)

_thread.start_new_thread(server, (['127.0.0.1', 8181, '127.0.0.1', 80],))
print("@"*80)
while True:
	time.sleep(60)
```

### Credit
- [vinodpandey](https://github.com/vinodpandey/python-port-forward)
