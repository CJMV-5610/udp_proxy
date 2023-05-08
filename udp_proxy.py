import socket
import argparse

SERVER_NAME = "minetest"
HOST = ""
BUFFER_SIZE = 1024

PARSER = argparse.ArgumentParser(
    prog="udp_proxy.py",
    description="Receives UDP packets sent to a source port and passes them to a destination port.",
)
PARSER.add_argument("source_port", type=int)
PARSER.add_argument("destination_port", type=int)


PROTOCOL_ID = b"\x4f\x45\x74\x03"


def isPlayerPosPacket(packet: bytes) -> bool:
    if not packet.startswith(PROTOCOL_ID):
        return False
    # TODO: Strip off packet header and then check for '#' as the first byte.
    return packet.find(b"#")


def start_forwarding(source_port: int, destination_port: int) -> None:
    source_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_socket.connect((SERVER_NAME, source_port))
    print(f"Connecting to {(HOST, source_port)}/udp...")

    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination_socket.bind((HOST, destination_port))
    print(f"Listening on {(HOST, destination_port)}/udp...")

    with open("/tmp/udp_proxy.log", "wb") as out_file:
        while True:
            (destination_data, destination_addr) = destination_socket.recvfrom(
                BUFFER_SIZE
            )
            source_socket.send(destination_data)

            (source_data, source_addr) = source_socket.recvfrom(BUFFER_SIZE)

            if isPlayerPosPacket(source_data):
                out_file.write(source_data + b'\n')
                packet = source_data[:9] + (len(source_data[9:]) * b'\x00')
                out_file.write(packet + b'\n')

            destination_socket.sendto(packet, destination_addr)


def main():
    args = PARSER.parse_args()
    source_port = args.source_port
    destination_port = args.destination_port
    start_forwarding(source_port, destination_port)


if __name__ == "__main__":
    main()
