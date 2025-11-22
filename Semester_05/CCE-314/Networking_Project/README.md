# Traceroute Lab in Python

**A Computer Networking Project - CCE-314 (Networking Sessional)**

A simplified traceroute implementation using Python and raw ICMP sockets that discovers the network path packets take from your computer to any destination on the Internet.

---

## 📖 Table of Contents

- [Project Description](#project-description)
- [How Traceroute Works](#how-traceroute-works)
- [Features](#features)
- [Technical Details](#technical-details)
- [Installation](#installation)
- [Usage](#usage)
- [Output Example](#output-example)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
- [Troubleshooting](#troubleshooting)
- [Learning Outcomes](#learning-outcomes)
- [References](#references)

---

## 🎯 Project Description

### Overview

This project implements a **traceroute utility** that traces the path data packets take from your computer to a destination host on the Internet. The program reveals every router (hop) along the network path by sending ICMP (Internet Control Message Protocol) packets with progressively increasing TTL (Time To Live) values.

### Purpose

The goal is to understand:
- How packets travel across networks through multiple routers
- The concept of TTL (Time To Live) in IP packets
- ICMP protocol and its role in network diagnostics
- Network topology and routing
- Round-trip time (RTT) measurement

### What It Does

1. **Sends ICMP Echo Request packets** with increasing TTL values (1, 2, 3, ...)
2. **Receives ICMP responses** from routers along the path
3. **Measures round-trip time** for each hop
4. **Displays the complete route** showing all intermediate routers
5. **Identifies when destination is reached**

---

## 🔍 How Traceroute Works

### The TTL Mechanism

Every IP packet has a **TTL (Time To Live)** field that:
- Starts at a specific value (e.g., 64, 128, or 255)
- Gets **decremented by 1** at each router
- When TTL reaches **0**, the router **discards the packet**
- The router sends back an **ICMP Time Exceeded** message to the sender

### Our Algorithm

```
For TTL = 1, 2, 3, ... up to MAX_HOPS:
    1. Create ICMP Echo Request packet
    2. Set TTL to current value
    3. Send packet to destination
    4. Wait for ICMP response:
       - ICMP Time Exceeded (Type 11) → Router along path
       - ICMP Echo Reply (Type 0) → Final destination
    5. Record router IP and round-trip time
    6. If destination reached, stop
```

### Visual Example

```
Your Computer  →  Router 1  →  Router 2  →  Router 3  →  Destination
                 (TTL=0)
TTL=1: Packet ──────────X
       Response ←────────┘ (ICMP Time Exceeded from Router 1)

TTL=2: Packet ──────────────────────X
       Response ←──────────────────┘ (ICMP Time Exceeded from Router 2)

TTL=3: Packet ──────────────────────────────────X
       Response ←──────────────────────────────┘ (ICMP Time Exceeded from Router 3)

TTL=4: Packet ──────────────────────────────────────────────────→ Destination
       Response ←──────────────────────────────────────────────┘ (ICMP Echo Reply)
```

---

## ✨ Features

### Core Features

✅ **ICMP Packet Creation** - Builds proper ICMP Echo Request packets with correct headers  
✅ **TTL Manipulation** - Sets TTL values from 1 to 30 (configurable)  
✅ **ICMP Response Handling** - Parses Time Exceeded and Echo Reply messages  
✅ **Round-Trip Time Calculation** - Measures delay to each hop in milliseconds  
✅ **Hostname Resolution** - Attempts to resolve IP addresses to hostnames  
✅ **Timeout Handling** - Detects unresponsive routers with configurable timeout  
✅ **Multiple Probes** - Sends 3 probes per hop for reliability  
✅ **Clean Output Format** - Professional table display of results  

### Technical Implementation

- **Raw Sockets** - Uses `SOCK_RAW` for low-level ICMP access
- **Checksum Calculation** - Implements Internet checksum algorithm
- **Packet Parsing** - Extracts ICMP headers from IP packets
- **Error Handling** - Graceful handling of timeouts and errors

---

## 🔧 Technical Details

### ICMP Packet Structure

```
ICMP Header (8 bytes):
┌─────────────┬─────────────┬─────────────────────────────┐
│  Type (8)   │  Code (8)   │      Checksum (16)          │
├─────────────┴─────────────┼─────────────────────────────┤
│     Identifier (16)        │   Sequence Number (16)      │
└────────────────────────────┴─────────────────────────────┘

ICMP Types Used:
- Type 8: Echo Request (what we send)
- Type 0: Echo Reply (from destination)
- Type 11: Time Exceeded (from routers)
```

### Key Algorithms

**1. Checksum Calculation:**
```python
def calculate_checksum(data):
    # Sum all 16-bit words
    # Add carry bits back
    # Take one's complement
    return checksum
```

**2. TTL Setting:**
```python
socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl_value)
```

**3. RTT Measurement:**
```python
send_time = time.time()
# ... send packet and wait for response ...
recv_time = time.time()
rtt = (recv_time - send_time) * 1000  # milliseconds
```

---

## 💻 Installation

### Prerequisites

- **Python 3.6+** installed
- **Linux/Unix/macOS** operating system (or WSL on Windows)
- **Root/Administrator privileges** (required for raw sockets)

### Check Python Version

```bash
python3 --version
```

Should show Python 3.6 or higher.

### Download the Project

```bash
# Clone or download the project files
cd /path/to/your/workspace

# Verify files exist
ls -la
# Should show: traceroute.py, README.md
```

### No Additional Libraries Needed

This project uses only **Python standard library**:
- `socket` - Network communication
- `struct` - Binary data packing
- `time` - Timing and delays
- `sys` - System operations
- `select` - Socket timeout handling
- `os` - Process ID

---

## 🚀 Usage

### Basic Command

```bash
sudo python3 traceroute.py <destination>
```

### Examples

**1. Trace route to Google:**
```bash
sudo python3 traceroute.py google.com
```

**2. Trace route to a specific IP:**
```bash
sudo python3 traceroute.py 8.8.8.8
```

**3. Trace route to any website:**
```bash
sudo python3 traceroute.py www.github.com
```

### Why `sudo` is Required

Raw sockets require **root privileges** because they:
- Bypass normal socket security restrictions
- Can create custom packets at the network layer
- Could potentially be used for network attacks

**Without sudo, you'll get:**
```
❌ ERROR: This program requires root/administrator privileges!
Please run with: sudo python3 traceroute.py <destination>
```

---

## 📊 Output Example

### Sample Run

```bash
$ sudo python3 traceroute.py google.com
```

### Expected Output

```
======================================================================
  TRACEROUTE LAB - Network Path Discovery
======================================================================

🎯 Tracing route to google.com (142.250.185.46)
📊 Maximum hops: 30 | Packet size: 64 bytes
⏱️  Timeout: 2.0s | Probes per hop: 3

======================================================================

Hop   IP Address                               RTT (ms)        Status
----------------------------------------------------------------------
1     192.168.0.1                                3.45 ms      
2     10.12.16.1                                18.23 ms      
3     172.16.45.2                               25.67 ms      
4     203.112.45.89                             45.32 ms      
5     142.250.185.46                            78.91 ms      ✓ DESTINATION

======================================================================
✅ Destination reached in 5 hops!
======================================================================
```

### Output Explanation

| Column | Description |
|--------|-------------|
| **Hop** | The hop number (router sequence) |
| **IP Address** | The router's IP (with hostname if resolved) |
| **RTT (ms)** | Average round-trip time in milliseconds |
| **Status** | Shows "✓ DESTINATION" when final host reached |

### Possible Messages

- **Normal hop:** Shows IP and RTT
- **Timeout:** `* * * Request timeout` (router doesn't respond)
- **Destination:** `✓ DESTINATION` marker appears

---

## 📁 Project Structure

```
Networking_Project/
│
├── traceroute.py          # Main traceroute implementation
├── README.md              # This documentation file
├── PRESENTATION_GUIDE.md  # Presentation preparation guide
├── VIVA_GUIDE.md          # Viva exam Q&A preparation
└── report.pdf             # Project report (to be added)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `traceroute.py` | Complete Python implementation of traceroute |
| `README.md` | Project documentation and usage guide |
| `PRESENTATION_GUIDE.md` | How to present this project (10+ min) |
| `VIVA_GUIDE.md` | Viva questions and answers |
| `report.pdf` | Detailed project report with diagrams |

---

## 🛠️ Implementation Details

### Main Components

#### 1. `calculate_checksum(data)`
Computes Internet checksum for ICMP packet validation.

```python
# Algorithm:
# 1. Sum all 16-bit words
# 2. Add overflow back to sum
# 3. Return one's complement
```

#### 2. `create_icmp_packet(packet_id, sequence)`
Constructs ICMP Echo Request packet with proper header.

```python
# Header: Type, Code, Checksum, ID, Sequence
# Data: Timestamp + padding
```

#### 3. `parse_icmp_header(data)`
Extracts ICMP type, code, and other fields from response.

#### 4. `send_probe(dest_addr, ttl, packet_id, sequence)`
Sends one ICMP packet with specific TTL and waits for response.

**Returns:**
- Router IP address
- Round-trip time
- Whether destination was reached

#### 5. `traceroute(destination)`
Main loop that:
- Resolves hostname to IP
- Tries TTL from 1 to MAX_HOPS
- Sends multiple probes per hop
- Displays results in table format

### Configuration Constants

```python
MAX_HOPS = 30        # Maximum hops to try
TIMEOUT = 2.0        # Wait time for response (seconds)
PACKET_SIZE = 64     # ICMP packet size (bytes)
TRIES_PER_HOP = 3    # Probes sent per hop
```

You can modify these in the code for different behavior.

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Problem 1: Permission Denied
```
❌ ERROR: This program requires root/administrator privileges!
```

**Solution:** Run with `sudo`
```bash
sudo python3 traceroute.py google.com
```

#### Problem 2: Command Not Found
```
python3: command not found
```

**Solution:** Install Python 3
```bash
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3

# On Fedora/CentOS:
sudo dnf install python3
```

#### Problem 3: Cannot Resolve Hostname
```
❌ ERROR: Cannot resolve hostname 'example123.com'
```

**Solution:** 
- Check internet connection
- Verify hostname spelling
- Try using IP address directly

#### Problem 4: All Hops Show Timeout
```
1     * * *                               Request timeout
2     * * *                               Request timeout
```

**Possible causes:**
- Firewall blocking ICMP
- Network doesn't allow traceroute
- Routers configured to not respond to ICMP

**Solution:**
- Try different destination
- Check firewall settings
- This is normal for some networks

#### Problem 5: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'xyz'
```

**This shouldn't happen** - the program uses only standard library. If it does:
- Verify Python 3 installation
- Check if running correct Python version

---

## 📚 Learning Outcomes

After completing this project, you will understand:

### Networking Concepts
✅ **IP Packet Structure** - How packets are constructed and routed  
✅ **TTL Mechanism** - How TTL prevents infinite loops  
✅ **ICMP Protocol** - Purpose and types of ICMP messages  
✅ **Network Topology** - How networks are interconnected  
✅ **Routing** - How packets find their way across the Internet  

### Programming Skills
✅ **Raw Socket Programming** - Low-level network access  
✅ **Binary Data Handling** - Packing/unpacking network packets  
✅ **Checksum Algorithms** - Data integrity verification  
✅ **Timeout Handling** - Asynchronous network operations  
✅ **Error Handling** - Robust error management  

### Practical Skills
✅ **Network Diagnostics** - Troubleshooting connectivity issues  
✅ **Performance Analysis** - Measuring network latency  
✅ **System Administration** - Understanding privilege requirements  

---

## 🎓 For Your Viva Exam

### Be Prepared to Explain

1. **What is traceroute and why is it useful?**
   - Network diagnostic tool
   - Shows path packets take
   - Helps identify network problems

2. **How does TTL work?**
   - Decremented at each router
   - Prevents infinite loops
   - Triggers ICMP Time Exceeded when reaches 0

3. **What is ICMP?**
   - Internet Control Message Protocol
   - Used for error messages and diagnostics
   - Part of IP layer, not transport layer

4. **Why do we need raw sockets?**
   - To create custom ICMP packets
   - Normal sockets don't allow this
   - Requires root privileges for security

5. **How is RTT calculated?**
   - Record time before sending packet
   - Record time when response arrives
   - RTT = receive_time - send_time

### Be Ready to Demo

- Run traceroute to different destinations
- Explain the output line by line
- Show what happens with unreachable hosts
- Modify constants (MAX_HOPS, TIMEOUT) and show effect

---

## 📖 References

### Assignment Source
- **Kurose & Ross** - Computer Networking: A Top-Down Approach
- Official Assignment: https://gaia.cs.umass.edu/kurose_ross/programming.php

### Technical Documentation
- **RFC 792** - Internet Control Message Protocol (ICMP)
- **RFC 791** - Internet Protocol (IP)
- **Python Socket Documentation** - https://docs.python.org/3/library/socket.html

### Additional Resources
- How Traceroute Works: https://www.youtube.com/watch?v=G05y9UKT69s
- ICMP Protocol Explained: https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol
- Raw Sockets Tutorial: https://www.binarytides.com/raw-sockets-python/

---

## 👨‍💻 Project Information

**Course:** CCE-314 (Networking Sessional)  
**Semester:** 5th Semester  
**Topic:** Traceroute Lab (Python)  
**Date:** November 2025  

**Key Requirements Met:**
✅ Original implementation (not copy-paste)  
✅ Fully functional and tested  
✅ Comprehensive documentation  
✅ Ready for live demonstration  
✅ Suitable for 10+ minute presentation  

---

## 📝 License

This project is created for educational purposes as part of the Computer Networking course assignment.

---

## 🤝 Acknowledgments

- Prof. Kurose & Ross for the assignment design
- Python community for excellent documentation
- Networking course instructors

---

**End of README**

For presentation guide, see: `PRESENTATION_GUIDE.md`  
For viva preparation, see: `VIVA_GUIDE.md`
