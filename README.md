
# Authoritative DNS Server (Python)

This project is a **simple authoritative DNS server** implemented in Python using raw sockets.
It listens for DNS queries on port **53 (UDP)** and responds with basic DNS response structures.
The goal of this code is to demonstrate how DNS packet parsing, flags, and response construction works at the protocol level.

---

## Features

* Implements a **UDP DNS server** bound to `127.0.0.1:53`.
* Parses **DNS packet headers** including:

  * Transaction ID
  * Flags
  * Question section
* Handles **basic domain name extraction** from queries.
* Demonstrates how to construct **DNS response flags** (QR, AA, TC, RD, RA, RCODE).
* Provides a foundation to extend with **A record responses** and other resource record types.

---

## Requirements

* Python 3.x

---

## Running the Server

1. Run the server:

   ```bash
   sudo python3 dns_server.py
   ```

   The server will start listening on `127.0.0.1:53`.

---

## Code Structure

* **`display()`**: Helper to print debug info.
* **`get_flags()`**: Builds the DNS flags for the response packet.
* **`get_domain_name()`**: Extracts the queried domain name and question type from the DNS packet.
* **`buildresponse()`**: Main function to parse an incoming request and construct a DNS response.
* **Main loop**: Runs a UDP listener for DNS requests and sends back responses.

---

## Limitations / Next Steps

* Only partially implements the DNS response logic (currently extracts queries, doesn’t return real answers).
* Only supports **A record (IPv4)** queries (`QTYPE 0x0001`) — needs to be extended for other record types.
* Runs only on `127.0.0.1` for testing (not production-ready).

---

## Learning & Experimentation

This server code is ideal for understanding:

- DNS packet format and flag manipulation at byte/bit level
- DNS query structure and domain encoding in binary packets
- UDP socket programming fundamentals in Python
