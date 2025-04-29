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