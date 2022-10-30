#!/usr/bin/env python3

from socket import create_connection, error
from struct import pack
from time import sleep


def main():
    try:
        conn = create_connection(("localhost", 1234))
    except error as err:
        print("Error: ", err.strerror)
        exit(-1)

    data = conn.recv(1024)
    print(data.decode("ascii"))
    while True:
        cmd = bytes(input("$ "), "ascii")
        if cmd == "exit":
            break
        try:
            conn.sendall(pack("!I", len(cmd)))
            conn.sendall(cmd)
            res_len = int.from_bytes(conn.recv(4), "big")
            res = conn.recv(res_len).decode("ascii")
            print(res)
        except error as err:
            print("Error: ", err.strerror)
            conn.close()
            exit(-2)
            sleep(0.25)

    conn.close()


#    input("Press Enter")

if __name__ == "__main__":
    main()
