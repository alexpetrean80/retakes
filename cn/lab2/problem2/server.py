#!/usr/bin/env python3

from socket import AF_INET, SOCK_STREAM, error, socket
from struct import pack
from threading import Event, Lock, Thread
from time import sleep

mylock = Lock()
e = Event()
e.clear()
threads = []
client_count = 0


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
    message = f"Hello client #{str(client_id)}"
    print(message)

    path_len = int.from_bytes(client_sock.recv(4), "big")
    path = client_sock.recv(path_len).decode("ascii")

    try:
        f = open(path, "rb")
        for line in f.readlines():
            result = line
            client_sock.sendall(pack("!I", len(result)))
            client_sock.sendall(result)
        client_sock.sendall(pack("!I", (len(b"done"))))
        client_sock.sendall(b"done")

        sleep(1)
        f.close()
        client_sock.close()
    except FileNotFoundError:
        client_sock.sendall(pack("!i", -1))
    finally:
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
