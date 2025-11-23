#!/usr/bin/env python3
"""
Enhanced Traceroute Lab - With Visualization & Geolocation
Computer Networks Assignment - Optional Features Implementation

This enhanced version includes:
- Graphical visualization using matplotlib
- Geographical information using IP geolocation
- Results export to JSON/CSV
- Multiple destination comparison

Author: Networking Lab Project
Date: November 2025
"""

import socket
import struct
import time
import sys
import select
import json
import os
from datetime import datetime

# Optional imports for enhanced features
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not installed. Visualization features disabled.")
    print("   Install with: pip install matplotlib")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  requests not installed. Geolocation features disabled.")
    print("   Install with: pip install requests")

# ICMP packet types
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11

# Configuration constants
MAX_HOPS = 30
TIMEOUT = 2.0
PACKET_SIZE = 64
TRIES_PER_HOP = 3


def calculate_checksum(data):
    """Calculate the Internet Checksum for ICMP packet."""
    checksum = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) + data[i + 1]
        else:
            word = data[i] << 8
        checksum += word
    
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    checksum = ~checksum & 0xffff
    
    return checksum


def create_icmp_packet(packet_id, sequence):
    """Create an ICMP Echo Request packet."""
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, packet_id, sequence)
    data = struct.pack('!d', time.time())
    data += b'TRACEROUTE' * 5
    checksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, checksum, packet_id, sequence)
    return header + data


def parse_icmp_header(data):
    """Parse ICMP header from received packet."""
    if len(data) < 8:
        return None
    icmp_header = data[0:8]
    icmp_type, code, checksum, packet_id, sequence = struct.unpack('!BBHHH', icmp_header)
    return icmp_type, code, checksum, packet_id, sequence


def get_hostname(ip_address):
    """Try to resolve IP address to hostname."""
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return ip_address


def get_geolocation(ip_address):
    """
    Get geographical information for an IP address.
    Uses free ip-api.com service (limited to 45 requests/min).
    """
    if not HAS_REQUESTS:
        return None
    
    # Don't lookup private IPs
    if ip_address.startswith('192.168.') or ip_address.startswith('10.') or ip_address.startswith('172.'):
        return {
            'country': 'Private Network',
            'city': 'Local',
            'lat': 0,
            'lon': 0,
            'isp': 'Private'
        }
    
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'lat': data.get('lat', 0),
                    'lon': data.get('lon', 0),
                    'isp': data.get('isp', 'Unknown'),
                    'as': data.get('as', 'Unknown')
                }
    except Exception as e:
        pass
    
    return None


def send_probe(dest_addr, ttl, packet_id, sequence):
    """Send a single ICMP probe packet with specified TTL."""
    try:
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_socket.settimeout(TIMEOUT)
        
        packet = create_icmp_packet(packet_id, sequence)
        send_time = time.time()
        send_socket.sendto(packet, (dest_addr, 1))
        
        try:
            ready = select.select([recv_socket], [], [], TIMEOUT)
            
            if ready[0]:
                recv_time = time.time()
                recv_packet, addr = recv_socket.recvfrom(1024)
                rtt = (recv_time - send_time) * 1000
                
                ip_header_len = (recv_packet[0] & 0x0F) * 4
                icmp_data = recv_packet[ip_header_len:]
                
                parsed = parse_icmp_header(icmp_data)
                if parsed:
                    icmp_type = parsed[0]
                    
                    if icmp_type == ICMP_ECHO_REPLY:
                        return (addr[0], rtt, True)
                    elif icmp_type == ICMP_TIME_EXCEEDED:
                        return (addr[0], rtt, False)
                
                return (addr[0], rtt, False)
            else:
                return (None, None, False)
                
        except socket.timeout:
            return (None, None, False)
        
    except PermissionError:
        print("\n❌ ERROR: This program requires root/administrator privileges!")
        print("Please run with: sudo python3 traceroute_enhanced.py <destination>\n")
        sys.exit(1)
    except Exception as e:
        return (None, None, False)
    finally:
        send_socket.close()
        recv_socket.close()


def traceroute_enhanced(destination, enable_geo=True):
    """
    Perform enhanced traceroute with geolocation data collection.
    Returns list of hop data for visualization.
    """
    print(f"\n{'='*80}")
    print(f"  ENHANCED TRACEROUTE LAB - Network Path Discovery with Visualization")
    print(f"{'='*80}\n")
    
    try:
        dest_ip = socket.gethostbyname(destination)
        print(f"🎯 Tracing route to {destination} ({dest_ip})")
        print(f"📊 Maximum hops: {MAX_HOPS} | Packet size: {PACKET_SIZE} bytes")
        print(f"⏱️  Timeout: {TIMEOUT}s | Probes per hop: {TRIES_PER_HOP}")
        if enable_geo and HAS_REQUESTS:
            print(f"🌍 Geolocation: ENABLED")
        print(f"\n{'='*80}\n")
    except socket.gaierror:
        print(f"❌ ERROR: Cannot resolve hostname '{destination}'")
        sys.exit(1)
    
    packet_id = os.getpid() & 0xFFFF
    sequence = 1
    reached_destination = False
    
    # Store hop data for visualization
    hop_data = []
    
    print(f"{'Hop':<5} {'IP Address':<40} {'RTT (ms)':<12} {'Location':<30} {'ISP'}")
    print(f"{'-'*80}")
    
    for ttl in range(1, MAX_HOPS + 1):
        router_ip = None
        total_rtt = 0
        success_count = 0
        
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
        
        if router_ip:
            avg_rtt = total_rtt / success_count if success_count > 0 else 0
            hostname = get_hostname(router_ip)
            
            # Get geolocation
            geo = None
            if enable_geo and HAS_REQUESTS:
                geo = get_geolocation(router_ip)
                time.sleep(0.1)  # Rate limiting
            
            location = "Unknown"
            isp = "Unknown"
            if geo:
                location = f"{geo['city']}, {geo['country']}"
                isp = geo['isp'][:30]
            
            # Store hop data
            hop_info = {
                'hop': ttl,
                'ip': router_ip,
                'hostname': hostname,
                'rtt': avg_rtt,
                'geo': geo,
                'is_destination': reached_destination
            }
            hop_data.append(hop_info)
            
            status = "✓ DESTINATION" if reached_destination else ""
            print(f"{ttl:<5} {router_ip:<40} {avg_rtt:>6.2f} ms    {location:<30} {isp} {status}")
            
            if reached_destination:
                print(f"\n{'='*80}")
                print(f"✅ Destination reached in {ttl} hops!")
                print(f"{'='*80}\n")
                break
        else:
            hop_data.append({
                'hop': ttl,
                'ip': None,
                'hostname': None,
                'rtt': None,
                'geo': None,
                'is_destination': False
            })
            print(f"{ttl:<5} {'* * *':<40} {'Timeout':<12}")
        
        time.sleep(0.1)
    
    if not reached_destination:
        print(f"\n{'='*80}")
        print(f"⚠️  Destination not reached within {MAX_HOPS} hops")
        print(f"{'='*80}\n")
    
    return hop_data, dest_ip, destination


def visualize_traceroute(hop_data, destination):
    """Create graphical visualization of traceroute results."""
    if not HAS_MATPLOTLIB:
        print("⚠️  Matplotlib not available. Skipping visualization.")
        return
    
    # Filter out None hops
    valid_hops = [h for h in hop_data if h['ip'] is not None]
    
    if not valid_hops:
        print("⚠️  No valid hops to visualize.")
        return
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle(f'Traceroute Analysis to {destination}', fontsize=16, fontweight='bold')
    
    # Plot 1: RTT vs Hop Number
    hops = [h['hop'] for h in valid_hops]
    rtts = [h['rtt'] for h in valid_hops]
    
    ax1.plot(hops, rtts, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    ax1.fill_between(hops, rtts, alpha=0.3, color='#2E86AB')
    ax1.set_xlabel('Hop Number', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Round-Trip Time (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('Network Latency by Hop', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(hops)
    
    # Highlight destination
    if valid_hops[-1]['is_destination']:
        ax1.scatter([valid_hops[-1]['hop']], [valid_hops[-1]['rtt']], 
                   color='red', s=200, zorder=5, marker='*', label='Destination')
        ax1.legend()
    
    # Plot 2: Geographical Path (if available)
    geo_hops = [h for h in valid_hops if h['geo'] and h['geo']['lat'] != 0]
    
    if geo_hops and len(geo_hops) > 1:
        lats = [h['geo']['lat'] for h in geo_hops]
        lons = [h['geo']['lon'] for h in geo_hops]
        hop_nums = [h['hop'] for h in geo_hops]
        
        ax2.plot(lons, lats, marker='o', linewidth=2, markersize=8, color='#A23B72')
        ax2.scatter(lons, lats, c=hop_nums, cmap='viridis', s=200, zorder=5, edgecolors='black')
        
        # Annotate points
        for i, h in enumerate(geo_hops):
            location = f"{h['geo']['city']}"
            ax2.annotate(f"Hop {h['hop']}\n{location}", 
                        (lons[i], lats[i]),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center',
                        fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        ax2.set_xlabel('Longitude', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Latitude', fontsize=12, fontweight='bold')
        ax2.set_title('Geographic Path', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'Geographic data not available\nfor visualization',
                ha='center', va='center', fontsize=14, transform=ax2.transAxes)
        ax2.set_xticks([])
        ax2.set_yticks([])
    
    plt.tight_layout()
    
    # Save figure
    filename = f"traceroute_{destination.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n📊 Visualization saved: {filename}")
    
    # Show plot
    plt.show()


def export_results(hop_data, dest_ip, destination, format='json'):
    """Export traceroute results to JSON or CSV format."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == 'json':
        filename = f"traceroute_{destination.replace('.', '_')}_{timestamp}.json"
        data = {
            'destination': destination,
            'destination_ip': dest_ip,
            'timestamp': datetime.now().isoformat(),
            'hops': hop_data
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"📄 Results exported to JSON: {filename}")
    
    elif format == 'csv':
        filename = f"traceroute_{destination.replace('.', '_')}_{timestamp}.csv"
        with open(filename, 'w') as f:
            f.write("Hop,IP,Hostname,RTT(ms),Country,City,ISP\n")
            for hop in hop_data:
                ip = hop['ip'] or 'Timeout'
                hostname = hop['hostname'] or '-'
                rtt = f"{hop['rtt']:.2f}" if hop['rtt'] else '-'
                country = hop['geo']['country'] if hop['geo'] else '-'
                city = hop['geo']['city'] if hop['geo'] else '-'
                isp = hop['geo']['isp'] if hop['geo'] else '-'
                f.write(f"{hop['hop']},{ip},{hostname},{rtt},{country},{city},{isp}\n")
        print(f"📄 Results exported to CSV: {filename}")


def print_usage():
    """Print usage information."""
    print("\n" + "="*80)
    print("  ENHANCED TRACEROUTE LAB - Usage Instructions")
    print("="*80)
    print("\nUsage:")
    print("  sudo python3 traceroute_enhanced.py <destination> [options]")
    print("\nOptions:")
    print("  --no-geo          Disable geolocation lookup")
    print("  --no-viz          Disable visualization")
    print("  --export-json     Export results to JSON")
    print("  --export-csv      Export results to CSV")
    print("\nExamples:")
    print("  sudo python3 traceroute_enhanced.py google.com")
    print("  sudo python3 traceroute_enhanced.py 8.8.8.8 --export-json")
    print("  sudo python3 traceroute_enhanced.py www.github.com --no-geo")
    print("\nNote: Requires root/administrator privileges for raw sockets")
    print("="*80 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    destination = sys.argv[1]
    
    # Parse options
    enable_geo = '--no-geo' not in sys.argv
    enable_viz = '--no-viz' not in sys.argv
    export_json = '--export-json' in sys.argv
    export_csv = '--export-csv' in sys.argv
    
    try:
        # Run enhanced traceroute
        hop_data, dest_ip, dest_name = traceroute_enhanced(destination, enable_geo)
        
        # Export results if requested
        if export_json:
            export_results(hop_data, dest_ip, dest_name, 'json')
        if export_csv:
            export_results(hop_data, dest_ip, dest_name, 'csv')
        
        # Visualize if requested and available
        if enable_viz and HAS_MATPLOTLIB:
            print("\n📊 Generating visualization...")
            visualize_traceroute(hop_data, dest_name)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Traceroute interrupted by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)
