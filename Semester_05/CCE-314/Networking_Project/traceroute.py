#!/usr/bin/env python3
"""
Traceroute Lab - Computer Networks Assignment
A simplified traceroute implementation using Python and raw ICMP sockets.

This program discovers the network path to a destination by sending ICMP Echo Request
packets with increasing TTL (Time To Live) values. Each router along the path returns
an ICMP Time Exceeded message when TTL reaches 0, revealing the route.

Author: Networking Lab Project
Date: November 2025
"""

import socket
import struct
import time
import sys
import select

# ICMP packet types
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11

# Configuration constants
MAX_HOPS = 30           # Maximum number of hops to try
TIMEOUT = 2.0           # Socket timeout in seconds
PACKET_SIZE = 64        # Size of ICMP packet
TRIES_PER_HOP = 3       # Number of probes per hop


def calculate_checksum(data):
    """
    Calculate the Internet Checksum for ICMP packet.
    
    The checksum is calculated by:
    1. Summing all 16-bit words in the data
    2. Adding any carry bits back to the sum
    3. Taking the one's complement
    
    Args:
        data: Bytes to calculate checksum for
        
    Returns:
        16-bit checksum value
    """
    checksum = 0
    # Process data in 16-bit chunks
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            # Combine two bytes into one 16-bit word
            word = (data[i] << 8) + data[i + 1]
        else:
            # Handle odd-length data
            word = data[i] << 8
        checksum += word
    
    # Add carry bits back to checksum
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    
    # Take one's complement
    checksum = ~checksum & 0xffff
    
    return checksum


def create_icmp_packet(packet_id, sequence):
    """
    Create an ICMP Echo Request packet.
    
    ICMP Header Format (8 bytes):
    - Type (8 bits): 8 for Echo Request
    - Code (8 bits): 0
    - Checksum (16 bits): Calculated checksum
    - Identifier (16 bits): Process ID
    - Sequence Number (16 bits): Packet sequence
    
    Args:
        packet_id: Unique identifier (usually process ID)
        sequence: Sequence number for this packet
        
    Returns:
        Complete ICMP packet as bytes
    """
    # Create header with checksum = 0 initially
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, packet_id, sequence)
    
    # Add payload data (timestamp for RTT calculation)
    data = struct.pack('!d', time.time())
    data += b'TRACEROUTE' * 5  # Padding to reach desired packet size
    
    # Calculate checksum for header + data
    checksum = calculate_checksum(header + data)
    
    # Recreate header with correct checksum
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, checksum, packet_id, sequence)
    
    return header + data


def parse_icmp_header(data):
    """
    Parse ICMP header from received packet.
    
    Args:
        data: Raw packet data
        
    Returns:
        Tuple of (type, code, checksum, packet_id, sequence)
    """
    if len(data) < 8:
        return None
    
    icmp_header = data[0:8]
    icmp_type, code, checksum, packet_id, sequence = struct.unpack('!BBHHH', icmp_header)
    
    return icmp_type, code, checksum, packet_id, sequence


def get_hostname(ip_address):
    """
    Try to resolve IP address to hostname.
    
    Args:
        ip_address: IP address string
        
    Returns:
        Hostname if found, otherwise IP address
    """
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return f"{hostname} ({ip_address})"
    except socket.herror:
        return ip_address


def send_probe(dest_addr, ttl, packet_id, sequence):
    """
    Send a single ICMP probe packet with specified TTL.
    
    Args:
        dest_addr: Destination IP address
        ttl: Time To Live value for this packet
        packet_id: Packet identifier
        sequence: Sequence number
        
    Returns:
        Tuple of (router_ip, rtt, reached_destination)
        Returns (None, None, False) on timeout
    """
    try:
        # Create raw socket for ICMP
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        
        # Create receive socket
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_socket.settimeout(TIMEOUT)
        
        # Send ICMP packet
        packet = create_icmp_packet(packet_id, sequence)
        send_time = time.time()
        send_socket.sendto(packet, (dest_addr, 1))
        
        # Wait for response
        try:
            # Use select for timeout handling
            ready = select.select([recv_socket], [], [], TIMEOUT)
            
            if ready[0]:
                recv_time = time.time()
                recv_packet, addr = recv_socket.recvfrom(1024)
                rtt = (recv_time - send_time) * 1000  # Convert to milliseconds
                
                # Extract IP header to get to ICMP data
                # IP header is typically 20 bytes (can be 20-60 with options)
                ip_header_len = (recv_packet[0] & 0x0F) * 4
                icmp_data = recv_packet[ip_header_len:]
                
                # Parse ICMP header
                parsed = parse_icmp_header(icmp_data)
                if parsed:
                    icmp_type = parsed[0]
                    
                    # Check if we reached destination (Echo Reply)
                    if icmp_type == ICMP_ECHO_REPLY:
                        return (addr[0], rtt, True)
                    # Check if this is a router (Time Exceeded)
                    elif icmp_type == ICMP_TIME_EXCEEDED:
                        return (addr[0], rtt, False)
                
                return (addr[0], rtt, False)
            else:
                # Timeout
                return (None, None, False)
                
        except socket.timeout:
            return (None, None, False)
        
    except PermissionError:
        print("\n❌ ERROR: This program requires root/administrator privileges!")
        print("Please run with: sudo python3 traceroute.py <destination>\n")
        sys.exit(1)
    except Exception as e:
        print(f"Error in send_probe: {e}")
        return (None, None, False)
    finally:
        send_socket.close()
        recv_socket.close()


def traceroute(destination):
    """
    Perform traceroute to destination host.
    
    Args:
        destination: Hostname or IP address
    """
    print(f"\n{'='*70}")
    print(f"  TRACEROUTE LAB - Network Path Discovery")
    print(f"{'='*70}\n")
    
    # Resolve destination hostname to IP
    try:
        dest_ip = socket.gethostbyname(destination)
        print(f"🎯 Tracing route to {destination} ({dest_ip})")
        print(f"📊 Maximum hops: {MAX_HOPS} | Packet size: {PACKET_SIZE} bytes")
        print(f"⏱️  Timeout: {TIMEOUT}s | Probes per hop: {TRIES_PER_HOP}")
        print(f"\n{'='*70}\n")
    except socket.gaierror:
        print(f"❌ ERROR: Cannot resolve hostname '{destination}'")
        sys.exit(1)
    
    # Use process ID as packet identifier
    packet_id = os.getpid() & 0xFFFF
    sequence = 1
    reached_destination = False
    
    print(f"{'Hop':<5} {'IP Address':<40} {'RTT (ms)':<15} {'Status'}")
    print(f"{'-'*70}")
    
    # Try each TTL from 1 to MAX_HOPS
    for ttl in range(1, MAX_HOPS + 1):
        router_ip = None
        total_rtt = 0
        success_count = 0
        
        # Send multiple probes per hop for reliability
        for attempt in range(TRIES_PER_HOP):
            result_ip, rtt, is_destination = send_probe(dest_ip, ttl, packet_id, sequence)
            sequence += 1
            
            if result_ip:
                router_ip = result_ip
                total_rtt += rtt
                success_count += 1
                
                if is_destination:
                    reached_destination = True
                    break
        
        # Display results for this hop
        if router_ip:
            avg_rtt = total_rtt / success_count if success_count > 0 else 0
            hostname = get_hostname(router_ip)
            status = "✓ DESTINATION" if reached_destination else ""
            
            print(f"{ttl:<5} {hostname:<40} {avg_rtt:>6.2f} ms      {status}")
            
            if reached_destination:
                print(f"\n{'='*70}")
                print(f"✅ Destination reached in {ttl} hops!")
                print(f"{'='*70}\n")
                break
        else:
            # No response (timeout)
            print(f"{ttl:<5} {'* * *':<40} {'Request timeout':<15}")
        
        time.sleep(0.1)  # Small delay between hops
    
    if not reached_destination:
        print(f"\n{'='*70}")
        print(f"⚠️  Destination not reached within {MAX_HOPS} hops")
        print(f"{'='*70}\n")


def print_usage():
    """Print usage information."""
    print("\n" + "="*70)
    print("  TRACEROUTE LAB - Usage Instructions")
    print("="*70)
    print("\nUsage:")
    print("  sudo python3 traceroute.py <destination>")
    print("\nExamples:")
    print("  sudo python3 traceroute.py google.com")
    print("  sudo python3 traceroute.py 8.8.8.8")
    print("  sudo python3 traceroute.py www.example.com")
    print("\nNote: Requires root/administrator privileges for raw sockets")
    print("="*70 + "\n")


if __name__ == "__main__":
    import os
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
    
    destination = sys.argv[1]
    
    try:
        traceroute(destination)
    except KeyboardInterrupt:
        print("\n\n⚠️  Traceroute interrupted by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)
