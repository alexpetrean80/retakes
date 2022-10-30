#!/usr/bin/env python3
from os import popen
from socket import AF_INET, SOCK_STREAM, error, socket
from struct import pack
from threading import Event, Lock, Thread
from time import sleep

mylock = Lock()
e = Event()
e.clear()
threads = []
client_count = 0


def exec(cmd):
    return popen(cmd).read()


def reset_srv():
    global mylock, threads, e, client_count
    while True:
        e.wait()
        for t in threads:
            t.join()
        print("all threads are finished now")
        e.clear()
        mylock.acquire()
        threads = []
        client_count = 0
        mylock.release()


def worker(client_sock):
    global mylock, e, client_count
    client_id = client_count
    print("client #", client_count, "from: ", client_sock.getpeername(), client_sock)
    message = "Hello client #" + str(client_id)
    client_sock.sendall(bytes(message, "ascii"))

    cmd_len = int.from_bytes(client_sock.recv(4), "big")
    cmd = client_sock.recv(cmd_len).decode("ascii")

    result = bytes(exec(cmd), "ascii")
    client_sock.sendall(pack("!I", len(result)))
    client_sock.sendall(result)
    sleep(1)
    client_sock.close()


def main():
    global client_count
    try:
        rs = socket(AF_INET, SOCK_STREAM)
        rs.bind(("0.0.0.0", 1234))
        rs.listen(5)
    except error as err:
        print(err.strerror)
        exit(1)

    reset_th = Thread(target=reset_srv, daemon=True)
    reset_th.start()
    while True:
        client_sock, _ = rs.accept()
        wt = Thread(target=worker, args=(client_sock,))
        wt.start()
        threads.append(wt)
        client_count += 1


if __name__ == "__main__":
    main()
