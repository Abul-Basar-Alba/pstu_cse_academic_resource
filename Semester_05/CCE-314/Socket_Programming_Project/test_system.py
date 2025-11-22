#!/usr/bin/env python3
"""
Test script to verify the election voting system
"""

import sys
import time
import requests
import json

def test_electorate(electorate_id, port):
    """Test a single electorate"""
    base_url = f"http://localhost:{port}"
    
    print(f"\n{'='*60}")
    print(f"Testing Electorate {electorate_id} on port {port}")
    print(f"{'='*60}")
    
    # Test 1: Get info
    try:
        response = requests.get(f"{base_url}/api/info", timeout=2)
        if response.status_code == 200:
            info = response.json()
            print(f"✓ Info API working: Electorate {info['electorate_id']}")
        else:
            print(f"✗ Info API failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to electorate {electorate_id}")
        print(f"  Make sure it's running: python3 app.py {electorate_id}")
        return False
    
    # Test 2: Get status
    try:
        response = requests.get(f"{base_url}/api/status", timeout=2)
        if response.status_code == 200:
            status = response.json()
            print(f"✓ Status API working: Has voted = {status['has_voted']}")
        else:
            print(f"✗ Status API failed")
            return False
    except Exception as e:
        print(f"✗ Status API error: {e}")
        return False
    
    # Test 3: Get results
    try:
        response = requests.get(f"{base_url}/api/results", timeout=2)
        if response.status_code == 200:
            results = response.json()
            print(f"✓ Results API working: Ready = {results['ready']}")
        else:
            print(f"✗ Results API failed")
            return False
    except Exception as e:
        print(f"✗ Results API error: {e}")
        return False
    
    return True

def main():
    print("\n" + "="*60)
    print("Election Voting System - Test Script")
    print("="*60)
    
    # Check if electorates are running
    electorates_to_test = [1, 2, 3, 4, 5]
    running_electorates = []
    
    for i in electorates_to_test:
        port = 5000 + i
        if test_electorate(i, port):
            running_electorates.append(i)
    
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}")
    print(f"Electorates running: {len(running_electorates)}/5")
    print(f"Running IDs: {running_electorates}")
    
    if len(running_electorates) == 5:
        print("\n✓ All electorates are running correctly!")
        print("\nYou can now open these URLs in your browser:")
        for i in range(1, 6):
            print(f"  • http://localhost:{5000+i} (Electorate {i})")
        print("\nReady for demo!")
    elif len(running_electorates) > 0:
        print(f"\n⚠ Only {len(running_electorates)} electorates are running")
        print("Start missing electorates with:")
        for i in electorates_to_test:
            if i not in running_electorates:
                print(f"  python3 app.py {i}")
    else:
        print("\n✗ No electorates are running!")
        print("\nStart all electorates with:")
        print("  ./scripts/run_all.sh")
        print("\nOr start them individually:")
        for i in range(1, 6):
            print(f"  python3 app.py {i}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("\n✗ 'requests' library not found!")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    main()
