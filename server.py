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


class TupleSpace:
    """Represents the tuple space with thread-safe operations."""

    def __init__(self):
        """Initialize an empty tuple space."""
        self.tuples = {}  # Dictionary to store key-value pairs
        self.lock = threading.Lock()  # Lock for thread safety

        # Statistics
        self.total_clients = 0
        self.total_operations = 0
        self.total_reads = 0
        self.total_gets = 0
        self.total_puts = 0
        self.total_errors = 0


def put(self, key, value):
    """
    Add a new tuple to the space if the key doesn't exist.
    Returns 0 if successful, 1 if the key already exists.
    """
    with self.lock:
        self.total_operations += 1
        self.total_puts += 1

        if key in self.tuples:
            self.total_errors += 1
            return 1  # Error: key already exists

        self.tuples[key] = value
        return 0  # Success


def get(self, key):
    """
    Remove a tuple from the space and return its value.
    Returns (value, True) if successful, (None, False) if the key doesn't exist.
    """
    with self.lock:
        self.total_operations += 1
        self.total_gets += 1

        if key not in self.tuples:
            self.total_errors += 1
            return None, False  # Error: key does not exist

        value = self.tuples[key]
        del self.tuples[key]
        return value, True  # Success


def read(self, key):
    """
    Read a tuple's value without removing it.
    Returns (value, True) if successful, (None, False) if the key doesn't exist.
    """
    with self.lock:
        self.total_operations += 1
        self.total_reads += 1

        if key not in self.tuples:
            self.total_errors += 1
            return None, False  # Error: key does not exist

        return self.tuples[key], True  # Success
def get_statistics(self):
    """Return statistics about the tuple space."""
    with self.lock:
        num_tuples = len(self.tuples)
        # Calculate average sizes
        if num_tuples > 0:
            avg_key_size = sum(len(k) for k in self.tuples.keys()) / num_tuples
            avg_value_size = sum(len(v) for v in self.tuples.values()) / num_tuples
            avg_tuple_size = avg_key_size + avg_value_size
        else:
            avg_key_size = 0
            avg_value_size = 0
            avg_tuple_size = 0
        return {
            "num_tuples": num_tuples,
            "avg_tuple_size": avg_tuple_size,
            "avg_key_size": avg_key_size,
            "avg_value_size": avg_value_size,
            "total_clients": self.total_clients,
            "total_operations": self.total_operations,
            "total_reads": self.total_reads,
            "total_gets": self.total_gets,
            "total_puts": self.total_puts,
            "total_errors": self.total_errors
        }