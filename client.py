import socket
import sys
import os

def create_message(command, key, value=None):
    """
    Create a properly formatted protocol message to send to the server.
    The message starts with a 3-digit length prefix (including itself).
    """
    if command == "PUT":
        if not value:
            return None
        data = f"{key} {value}"
        message = f"P {data}"
    elif command == "GET":
        message = f"G {key}"
    elif command == "READ":
        message = f"R {key}"
    else:
        return None

    # Construct the final message without a space after size
    full_message = f"{len(message) + 3:03d}{message}"
    return full_message

def main():
    """
    Main client function:
    - Connects to the server
    - Reads commands from a file line by line
    - Sends request and waits for response before next (synchronous)
    - Displays server's response for each line
    """
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <input_file>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    input_file = sys.argv[3]

    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    try:
        with socket.create_connection((host, port)) as s, open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(" ", 2)
                if len(parts) < 2:
                    print(f"Invalid line: {line}")
                    continue

                command = parts[0]
                key = parts[1]
                value = parts[2] if command == "PUT" and len(parts) > 2 else None

                if command == "PUT" and value:
                    if len(key) + len(value) + 1 > 970:
                        print(f"PUT {key} {value}: ERROR too long, ignored")
                        continue

                msg = create_message(command, key, value)
                if not msg:
                    print(f"Invalid command: {line}")
                    continue

                s.sendall(msg.encode())

                # Receive the 3-byte header
                size = s.recv(3)
                if not size:
                    break
                total_size = int(size.decode())
                remaining = total_size - 3
                data = b""

                # Receive the rest of the message
                while remaining > 0:
                    chunk = s.recv(remaining)
                    if not chunk:
                        break
                    data += chunk
                    remaining -= len(chunk)

                    response = data.decode()
                    print(f"{line}: {response.strip()}")







