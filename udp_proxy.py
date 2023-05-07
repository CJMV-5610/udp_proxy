import socket
import argparse
import selectors

"""
minetest_nmpr  ---( SOURCE )-->  server_proxy  ---(  DEST  )-->  minetest_client

minetest_npmr  <--( SOURCE )---  server_proxy  <--(  DEST  )---  minetest_client
"""

HOST = ""
BUFFER_SIZE = 1024

SELECTOR = selectors.DefaultSelector()

PARSER = argparse.ArgumentParser(
    prog="udp_proxy.py",
    description="Receives UDP packets sent to a source port and passes them to a destination port.",
)
PARSER.add_argument("source_port", type=int)
PARSER.add_argument("destination_port", type=int)


def start_forwarding(source_port: int, destination_port: int) -> None:
    source_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_socket.bind((HOST, source_port))
    # SELECTOR.register(source_socket, selectors.EVENT_READ)
    print(f'Listening on {(HOST, source_port)}/udp...')

    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination_socket.bind((HOST, destination_port))
    # SELECTOR.register(destination_socket, selectors.EVENT_READ)
    print(f'Listening on {(HOST, destination_port)}/udp...')

    while True:
        (source_data, source_addr) = source_socket.recvfrom(BUFFER_SIZE)
        (destination_data, destination_addr) = destination_socket.recvfrom(BUFFER_SIZE)

        if not source_data and not destination_data:
            continue

        print(f"Source {source_addr} data:\n{source_data}\n")
        print(f"Destination {destination_addr} data:\n{destination_data}")


def main():
    args = PARSER.parse_args()
    source_port = args.source_port
    destination_port = args.destination_port
    start_forwarding(source_port, destination_port)


if __name__ == "__main__":
    main()
