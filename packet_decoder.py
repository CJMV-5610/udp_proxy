PROTOCOL_ID = bytes(b"\x4f\x45\x74\x03")
TOSERVER_PLAYERPOS_ID = 0x23


def is_protocol_packet(packet: bytes) -> bool:
    return packet.startswith(PROTOCOL_ID)


class S32:
    def __init__(self, data: bytes) -> None:
        if len(data) != S32.byte_length():
            raise ValueError(len(data))
        self._value = (
            (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | (data[3] << 0)
        )

    @staticmethod
    def byte_length() -> int:
        """
        The number of bytes needed to store 32 bits.
        """
        return 4

    def value(self) -> int:
        return self._value

    def __imul__(self, other):
        self._value = int(self._value * other)
        return self

    def __bytes__(self) -> bytes:
        return self.value().to_bytes(S32.byte_length(), "big", signed=False)

    def __repr__(self) -> str:
        return f"{self.value()}"

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, S32):
            return self.value() == __value.value()
        if isinstance(__value, int):
            return self.value() == __value
        return False


class V3S32:
    def __init__(self, data: bytes) -> None:
        if len(data) != V3S32.byte_length():
            raise ValueError(len(data))

        self.x = S32(data[0:4])
        self.y = S32(data[4:8])
        self.z = S32(data[8:12])

    @staticmethod
    def byte_length() -> int:
        """
        The number of bytes needed to store a 3D vector of 32-bit strings.
        """
        return 3 * S32.byte_length()

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __bytes__(self) -> bytes:
        return bytes(self.x) + bytes(self.y) + bytes(self.z)

    def __repr__(self) -> str:
        return f"V3S32({repr(self.x)}, {repr(self.y)}, {repr(self.z)})"

    def __str__(self) -> str:
        return (
            f"({self.x.value() / 100}, {self.y.value() / 100}, {self.z.value() / 100})"
        )


class TOSERVER_PLAYERPOS:
    def __init__(self, data: bytes) -> None:
        packet = data.split(b"\x23")[-1]
        if len(packet) != 24:
            raise ValueError(len(packet))

        self.position = V3S32(packet[0:12])
        self.speed = V3S32(packet[12:24])

    @staticmethod
    def byte_length() -> int:
        """
        The number of bytes needed to store two 3D vectors of 32-bit strings.
        """
        return 2 * V3S32.byte_length()

    @staticmethod
    def matches(packet: bytes) -> bool:
        if not is_protocol_packet(packet):
            return False
        if len(packet) < 9:
            return False
        return packet[9] == TOSERVER_PLAYERPOS_ID

    def scale_speed(self, factor) -> None:
        self.speed *= factor

    def __bytes__(self) -> bytes:
        return bytes(self.position) + bytes(self.speed)

    def __repr__(self) -> str:
        return f"TOSERVER_PLAYERPOS(\n\t{repr(self.position)},\n\t{repr(self.speed)}\n)"

    def __str__(self) -> str:
        return f"({self.position}, {self.speed})"