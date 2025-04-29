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