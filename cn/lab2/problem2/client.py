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

    path = input("path=")
    try:
        path_bytes = bytes(path, "ascii")
        conn.sendall(pack("!i", len(path_bytes)))
        conn.sendall(path_bytes)

        with open(f"{path}.copy", "w") as f:
            while True:
                res_len = int.from_bytes(conn.recv(4), "big")

                if res_len == 0:
                    print("File does not exist")
                    break

                res = conn.recv(res_len).decode("ascii")

                if res == "done":
                    break
                f.write(res)

    except error as err:
        print("Error: ", err.strerror)
        conn.close()
        sleep(0.25)
        exit(-2)
    conn.close()


#    input("Press Enter")

if __name__ == "__main__":
    main()
