import socket

HOST = '127.0.0.1'
PORT = 8088


def session(sock):
    while True:
        cmd = input("> ")
        sock.send(cmd.encode('utf-8'))
        totalData = []
        data = sock.recv(1024)
        print(data.decode('utf-8'))
        if cmd.lower() == "end":
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                totalData.append(data.decode('utf-8'))
            print("".join(totalData))
            break

def Main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    session(sock)
    sock.close()

if __name__ == '__main__':
    Main()
