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