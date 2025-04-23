"""
COMPX234-A3: Tuple Space Server
A server implementing a tuple space using TCP sockets and multi-threading.

This server maintains a collection of key-value pairs (tuples) and allows
clients to perform operations on them (PUT, GET, READ) via a network protocol.
"""
import socket
import threading
import time
import sys
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class ProtocolError(Exception):
    """Exception raised for errors in the protocol format."""
    pass

class TupleSpace:
    """Represents the tuple space with thread-safe operations."""

    def __init__(self):
        """Initialize an empty tuple space."""
        self.tuples = {}  # Dictionary to store key-value pairs
        self.lock = threading.Lock()  # Lock for thread safety