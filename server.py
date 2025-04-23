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