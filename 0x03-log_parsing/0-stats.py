#!/usr/bin/python3

import sys
import signal

# Initialize metrics
total_size = 0
status_counts = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

def print_statistics():
    """Prints the current statistics."""
    print(f"Total file size: {total_size}")
    for status_code in sorted(status_counts.keys()):
        if status_counts[status_code] > 0:
            print(f"{status_code}: {status_counts[status_code]}")

def signal_handler(sig, frame):
    """Handles keyboard interruption (CTRL + C)."""
    print_statistics()
    sys.exit(0)

# Register the signal handler for keyboard interruption
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        parts = line.split()
        
        if len(parts) < 7:
            continue
        
        ip, dash, date, method, url, protocol, status, size = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7]
        
        # Check the format of the line
        if dash != '-' or not date.startswith('[') or not date.endswith(']') or method != '"GET' or url != '/projects/260' or protocol != 'HTTP/1.1"':
            continue
        
        try:
            status = int(status)
            size = int(size)
        except ValueError:
            continue
        
        # Update metrics
        total_size += size
        if status in status_counts:
            status_counts[status] += 1
        
        line_count += 1
        
        if line_count % 10 == 0:
            print_statistics()

except KeyboardInterrupt:
    print_statistics()
    sys.exit(0)

# Print final statistics if there are any remaining lines
if line_count % 10 != 0:
    print_statistics()
