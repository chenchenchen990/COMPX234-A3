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


def handle_client(client_socket, addr, tuple_space):
    """Handle a single client connection."""
    logging.info(f"New connection from {addr}")

    try:
        while True:
            # Receive the message size (first 3 bytes)
            size_bytes = client_socket.recv(3)
            if not size_bytes or len(size_bytes) < 3:  # Client disconnected or incomplete message
                break

            try:
                # Parse the message size
                try:
                    message_size = int(size_bytes.decode())
                except ValueError:
                    raise ProtocolError("Invalid message size format")

                if message_size < 7 or message_size > 999:
                    raise ProtocolError("Message size must be between 7 and 999")

                # Rest of the message handling will be implemented here

            except ProtocolError as pe:
                error_message = str(pe)
                response = f"{len(error_message) + 8:03d} ERR {error_message}"
                client_socket.send(response.encode())
    except ConnectionResetError:
        logging.info(f"Connection reset by {addr}")
    except ConnectionAbortedError:
        logging.info(f"Connection aborted by {addr}")
    except BrokenPipeError:
        logging.info(f"Broken pipe with {addr}")
    except Exception as e:
        logging.error(f"Error handling client {addr}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection from {addr} closed")
    # Calculate how many more bytes we need to receive
    remaining_bytes = message_size - 3

    if remaining_bytes <= 0:
        raise ProtocolError("Invalid message size")

    # Receive the command and the rest of the message
    command_and_data = b""
    bytes_received = 0

    # Keep receiving until we get all the data or socket closes
    while bytes_received < remaining_bytes:
        chunk = client_socket.recv(min(1024, remaining_bytes - bytes_received))
        if not chunk:  # Socket closed
            return
        command_and_data += chunk
        bytes_received += len(chunk)

    # Decode the data
    try:
        command_and_data = command_and_data.decode()
    except UnicodeDecodeError:
        raise ProtocolError("Invalid message encoding")
    # Parse the command
    if not command_and_data or len(command_and_data) < 1:
        raise ProtocolError("Missing command")

    command = command_and_data[0]

    # Ensure there's a space after the command
    if len(command_and_data) > 1 and command_and_data[1] != ' ':
        raise ProtocolError("Expected space after command")

    # Get the data part (skip the space if present)
    data = command_and_data[2:] if len(command_and_data) > 2 else ""

    response = ""

    # Command processing will be implemented here
    # Process commands
    if command == 'R':  # READ
        key = data
        value, success = tuple_space.read(key)

        if success:
            response_text = f"OK ({key}, {value}) read"
        else:
            response_text = f"ERR {key} does not exist"

        response = f"{len(response_text) + 4:03d} {response_text}"
    elif command == 'G':  # GET
        key = data
        value, success = tuple_space.get(key)

        if success:
            response_text = f"OK ({key}, {value}) removed"
        else:
            response_text = f"ERR {key} does not exist"

        response = f"{len(response_text) + 4:03d} {response_text}"
    elif command == 'P':  # PUT
        # Split key and value
        space_pos = data.find(' ')
        if space_pos != -1:
            key = data[:space_pos]
            value = data[space_pos + 1:]

            # Validate key and value lengths
            if len(key) > 999:
                raise ProtocolError("Key too long (max 999 characters)")

            if len(key) + len(value) + 1 > 970:  # +1 for the space between them
                raise ProtocolError("Key and value combined too long (max 970 characters)")

            result = tuple_space.put(key, value)

            if result == 0:
                response_text = f"OK ({key}, {value}) added"
            else:
                response_text = f"ERR {key} already exists"

            response = f"{len(response_text) + 4:03d} {response_text}"
        else:
            raise ProtocolError("Invalid PUT format, missing value")
    else:
        raise ProtocolError(f"Unknown command '{command}'")

    # Send the response
    client_socket.send(response.encode())


def display_statistics(tuple_space):
    """Display statistics about the tuple space every 10 seconds."""
    while True:
        time.sleep(10)
        stats = tuple_space.get_statistics()

        print("\n----- Tuple Space Statistics -----")
        print(f"Number of tuples: {stats['num_tuples']}")
        print(f"Average tuple size: {stats['avg_tuple_size']:.2f}")
        print(f"Average key size: {stats['avg_key_size']:.2f}")
        print(f"Average value size: {stats['avg_value_size']:.2f}")
        print(f"Total clients connected: {stats['total_clients']}")
        print(f"Total operations: {stats['total_operations']}")
        print(f"Total READs: {stats['total_reads']}")
        print(f"Total GETs: {stats['total_gets']}")
        print(f"Total PUTs: {stats['total_puts']}")
        print(f"Total errors: {stats['total_errors']}")
        print("---------------------------------\n")


def shutdown_server(server_socket, tuple_space):
    """Properly shut down the server."""
    print("\nShutting down server...")

    # Print final statistics
    stats = tuple_space.get_statistics()
    print("\n----- Final Tuple Space Statistics -----")
    print(f"Number of tuples: {stats['num_tuples']}")
    print(f"Average tuple size: {stats['avg_tuple_size']:.2f}")
    print(f"Average key size: {stats['avg_key_size']:.2f}")
    print(f"Average value size: {stats['avg_value_size']:.2f}")
    print(f"Total clients connected: {stats['total_clients']}")
    print(f"Total operations: {stats['total_operations']}")
    print(f"Total READs: {stats['total_reads']}")
    print(f"Total GETs: {stats['total_gets']}")
    print(f"Total PUTs: {stats['total_puts']}")
    print(f"Total errors: {stats['total_errors']}")
    print("---------------------------------------")

    # Close the server socket
    if server_socket:
        server_socket.close()


def main():
    """Main function to run the server."""
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        return

    try:
        port = int(sys.argv[1])
        if not (50000 <= port <= 59999):
            print("Port must be between 50000 and 59999")
            return
    except ValueError:
        print("Port must be an integer")
        return
        # Create the tuple space
        tuple_space = TupleSpace()

        # Create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(5)
            logging.info(f"Server started on port {port}")
            while True:
                # Accept a client connection
                client_socket, addr = server_socket.accept()

                # Increment the client counter
                with tuple_space.lock:
                    tuple_space.total_clients += 1

                # Start a new thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, tuple_space))
                client_thread.daemon = True
                client_thread.start()



        except KeyboardInterrupt:
            shutdown_server(server_socket, tuple_space)
        except Exception as e:
            logging.error(f"Error: {e}")
            shutdown_server(server_socket, tuple_space)
        finally:
            server_socket.close()
    # Start statistics display thread
    stats_thread = threading.Thread(target=display_statistics, args=(tuple_space,), daemon=True)
    stats_thread.start()

if __name__ == "__main__":
    main()


def read(self, key):
    """
    Read a tuple's value without removing it.
    Returns (value, True) if successful, (None, False) if the key doesn't exist.
    """
    with self.lock:  # Ensure thread safety for all operations
        self.total_operations += 1
        self.total_reads += 1

        if key not in self.tuples:
            self.total_errors += 1
            return None, False  # Error: key does not exist

        return self.tuples[key], True  # Success


