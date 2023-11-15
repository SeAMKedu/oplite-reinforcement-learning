import socket

import config


def send_actions(actions: list, simsoft: str):
    """
    Send rover's actions to the simulation software.

    :param actions: List of actions that leads the rover to the goal.
    :param simsoft: Abbreviation of the simulation software.

    """
    host = "127.0.0.1"
    port = 0

    if simsoft == config.get("plant_simulation.name"):
        host = config.get("plant_simulation.host")
        port = config.get("plant_simulation.port")
    elif simsoft == config.get("visual_components.name"):
        host = config.get("visual_components.host")
        port = config.get("visual_components.port")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    errnum = client.connect_ex((host, port))
    if errnum == 0:
        message = ",".join([str(action) for action in actions])
        client.sendall(message.encode())
    else:
        print(f"Connection error: {errnum}")
