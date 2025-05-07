# MyclientServerProject2
 By Liu Jiachen 20233006445 Assignment3
# COMPX234-A3: Tuple Space Client/Server Implementation

## 1. Project Overview
This project implements a **Tuple Space Server** using TCP sockets and multi-threading in Python 3. The server stores key-value pairs (tuples) and allows multiple clients to interact concurrently through three operations:

1. `PUT`: Add a tuple if the key does not already exist
2. `GET`: Retrieve and remove a tuple if it exists
3. `READ`: Retrieve a tuple without removing it

The server uses a custom protocol with strict message formatting and maintains statistics about operations.

## 2. Project Structure
```
├── server.py          # Tuple Space Server implementation
├── client.py          # Tuple Space Client implementation
├── run_tests.py       # Batch test runner for multiple client files
├── test-workload-1/   # Test files directory
│   └── test-workload/
│       ├── client_1.txt
│       ├── client_2.txt
│       └── ...        # (up to client_10.txt)
└── README.md
```

## 3. Requirements
1. Python 3.6 or higher
2. Works on Windows, macOS, Linux

## 4. How to Run

### 4.1 Start the Server
```bash
python server.py 51234
```
The server will start on port 51234 and display statistics every 10 seconds.

### 4.2 Run a Single Client
```bash
python client.py localhost 51234 test-workload-1/test-workload/client_1.txt
```
This will connect to the server and execute the commands in the given file.

### 4.3 Run All Tests
```bash
python run_tests.py
```
This script will run all client test files 1-10 in sequence.

## 5. Implementation Details

### 5.1 Protocol Format
Messages between client and server follow this structure:
```
NNN COMMAND [key] [value]
```
Where:
1. `NNN`: 3-digit message length (includes the length digits themselves)
2. `COMMAND`: Single character - P (PUT), G (GET), or R (READ)
3. A space follows the command character
4. `key`: The tuple key (string)
5. `value`: For PUT operations only, the tuple value (string)

Examples:
```
# PUT Request
012 P key value

# GET Request
007 G key

# READ Request
007 R key
```

### 5.2 Server Responses
The server responds with these formats:
```
# Successful operations
NNN OK (k, v) read       # For READ
NNN OK (k, v) removed    # For GET
NNN OK (k, v) added      # For PUT

# Failed operations
NNN ERR k already exists    # For PUT when key exists
NNN ERR k does not exist    # For READ/GET when key doesn't exist
```

### 5.3 Server Implementation
1. **TupleSpace Class**
   Thread-safe storage using dictionary with lock
   Methods for put, get, read operations
   Statistics collection

2. **Client Handling**
   Each client connection spawns a new thread
   Protocol parsing and message handling
   Error management

3. **Statistics Display**
   Displays current tuple space statistics
   Shows tuple counts, average sizes, operation counts

### 5.4 Client Implementation
1. Reads commands from a file line by line
2. Creates protocol-compliant messages
3. Validates input constraints (key-value combined length ≤ 970)
4. Sends requests and waits for responses (synchronous behavior)
5. Displays operation results

## 6. Development Process

### 6.1 Understanding Requirements
1. Analyzed the tuple space concept and operations
2. Studied the required protocol format
3. Identified thread safety requirements
4. Understood message size constraints

### 6.2 Server Development
1. Implemented the TupleSpace class with thread-safe operations
2. Created the server socket and client connection handling
3. Added statistics collection and display
4. Implemented protocol parsing with proper error handling

### 6.3 Client Development
1. Created message formatting function
2. Implemented file parsing and validation
3. Added socket communication with error handling
4. Ensured synchronous operation (wait for response before next request)

### 6.4 Testing
1. Tested with individual operations
2. Performed concurrent access testing
3. Validated protocol compliance
4. Verified proper error handling
5. Ran the provided test workload

## 7. Sample Output

### 7.1 System Output
When running the test files against the server, the output shows each operation and its result:

```
READ podargidae: OK (podargidae, frogmouths) read
GET massif_central: OK (massif_central, a mountainous plateau in southern France that covers almost one sixth of the country) removed
GET de_spinoza: OK (de_spinoza, Dutch philosopher who espoused a pantheistic system (1632-1677)) removed
GET potty_chair: OK (potty_chair, toilet consisting of a small seat used by young children) removed
READ gin_and_tonic: OK (gin_and_tonic, gin and quinine water) read
GET drepanididae: ERR drepanididae does not exist
PUT massif_central a mountainous plateau in southern France that covers almost one sixth of the country: OK (massif_central, a mountainous plateau in southern France that covers almost one sixth of the country) added
READ potty_chair: ERR potty_chair does not exist
READ grazier: OK (grazier, a rancher who grazes cattle or sheep for market) read
GET mulberry_tree: ERR mulberry_tree does not exist
GET linkup: ERR linkup does not exist
PUT microphoning the transduction of sound waves into electrical waves (by a microphone): OK (microphoning, the transduction of sound waves into electrical waves (by a microphone)) added
PUT ventricular_fold either of the upper two vocal cords that are not involved in vocalization: OK (ventricular_fold, either of the upper two vocal cords that are not involved in vocalization) added
```

The server displays statistics:

```
----- Tuple Space Statistics -----
Number of tuples: 43
Average tuple size: 76.12
Average key size: 10.44
Average value size: 65.67
Total clients connected: 10
Total operations: 1000000
Total READs: 333260
Total GETs: 333829
Total PUTs: 332911
Total errors: 500118
---------------------------------
```

## 8. Implementation Challenges

### 8.1 Thread Safety
1. Implemented proper locking mechanisms for the shared tuple space
2. Used Python's threading.Lock to prevent race conditions
3. Ensured atomic operations for statistics updates

### 8.2 Protocol Handling
1. Carefully implemented the size-prefixed message format
2. Added robust error handling for malformed messages
3. Correctly parsed variable-length messages

### 8.3 Connection Management
1. Properly handled client disconnections
2. Implemented daemon threads to prevent orphaned processes
3. Added graceful server shutdown with final statistics

## 9. Verification and Validation

### 9.1 Testing Results
The implementation successfully passes all tests:
1. All operations (PUT, GET, READ) function correctly
2. Multiple concurrent clients operate without interference
3. Protocol errors are handled gracefully
4. Server maintains accurate statistics

### 9.2 Protocol Compliance
1. Message formats strictly follow the specification
2. Response messages match the required format
3. Error handling aligns with the protocol definition

## 10. Conclusion
This implementation successfully meets all requirements specified in the assignment. The server can handle multiple clients concurrently, and the clients can interact with the tuple space through the defined protocol with proper synchronous behavior.
