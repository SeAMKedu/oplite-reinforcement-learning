import json
import socket

import config
import helpers
from qlearning import QLearning


def main():
    host = config.get("server.host")
    port = config.get("server.port")

    # TCP/IP server socket.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    print(f"Server is listening on {host}:{port}")

    try:
        while True:
            try:
                # Receive a message from the simulation software.
                sock, _ = server.accept()
                sock.setblocking(False)
                data = sock.recv(1024)
                message = json.loads(data.decode())
                mapdata = message["mapdata"]
                mapsize = message["mapsize"]
                simsoft = message["simsoft"]
                print(f"\n{message}")

                # Use Q-learning to find actions from start to end point.
                qlearn = QLearning(mapdata)
                actions = qlearn.find_actions()

                # Send actions to simulation model.
                if qlearn.actions_found:
                    helpers.send_actions(actions, simsoft)

            except BlockingIOError:
                pass
    except KeyboardInterrupt:
        pass

    server.close()


if __name__ == "__main__":
    main()
