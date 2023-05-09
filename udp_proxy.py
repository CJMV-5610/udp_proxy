from packet_decoder import TOSERVER_PLAYERPOS

import argparse
import socket

SERVER_NAME = "minetest"
HOST = ""
BUFFER_SIZE = 1024

PARSER = argparse.ArgumentParser(
    prog="udp_proxy.py",
    description="Receives UDP packets sent to a source port and passes them to a destination port.",
)
PARSER.add_argument("source_port", type=int)
PARSER.add_argument("destination_port", type=int)


def start_forwarding(source_port: int, destination_port: int) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.connect((SERVER_NAME, source_port))
    print(f"Connecting to {(HOST, source_port)}/udp...")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((HOST, destination_port))
    print(f"Listening on {(HOST, destination_port)}/udp...")

    with open("/tmp/udp_proxy.log", "wb") as log_file:
        while True:
            (client_data, client_addr) = client_socket.recvfrom(BUFFER_SIZE)

            # TODO: Adversarial modification of client position packets
            if TOSERVER_PLAYERPOS.matches(client_data):
                packet = TOSERVER_PLAYERPOS(client_data)
                print("Speeding up player!")
                packet.scale_speed(1.2)
                try:
                    client_data = bytes(packet)
                except OverflowError as err:
                    print(f"OverflowError: {','.join(err.args)}")

            server_socket.send(client_data)
            log_file.write(client_data)
            server_data = server_socket.recvfrom(BUFFER_SIZE)[0]
            client_socket.sendto(server_data, client_addr)


def main():
    args = PARSER.parse_args()
    source_port = args.source_port
    destination_port = args.destination_port
    start_forwarding(source_port, destination_port)


if __name__ == "__main__":
    main()
