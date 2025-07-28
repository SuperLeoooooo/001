#!/usr/bin/env python3
"""
Simple command-line IP formatter.
Usage: python format_ip.py [IP_ADDRESS]
"""

import sys
from ip_formatter import IPFormatter


def format_single_ip(ip_str: str):
    """Format a single IP address and display results."""
    formatter = IPFormatter()
    
    print(f"Input: {ip_str}")
    print("-" * 30)
    
    if formatter.is_valid_ipv4(ip_str):
        print("Type: IPv4")
        normalized = formatter.normalize_ipv4(ip_str)
        print(f"Normalized: {normalized}")
        
        # Show with common subnet masks
        common_masks = [24, 16, 8]
        print("Common CIDR formats:")
        for mask in common_masks:
            cidr = formatter.format_ip_with_mask(normalized, mask)
            if cidr:
                print(f"  /{mask}: {cidr}")
                
    elif formatter.is_valid_ipv6(ip_str):
        print("Type: IPv6")
        normalized = formatter.normalize_ipv6(ip_str)
        expanded = formatter.expand_ipv6(ip_str)
        compressed = formatter.compress_ipv6(ip_str)
        
        print(f"Normalized: {normalized}")
        print(f"Expanded: {expanded}")
        print(f"Compressed: {compressed}")
        
    else:
        print("Status: Invalid IP address")
        print("Attempting to extract valid IPs from input...")
        extracted = formatter.extract_ips_from_text(ip_str)
        if extracted:
            print(f"Found valid IPs: {extracted}")
            for ip in extracted:
                print(f"\nFormatting: {ip}")
                format_single_ip(ip)
        else:
            print("No valid IP addresses found.")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("IP Address Formatter")
        print("Usage: python format_ip.py [IP_ADDRESS]")
        print("\nExamples:")
        print("  python format_ip.py 192.168.001.001")
        print("  python format_ip.py 2001:db8::1")
        print("  python format_ip.py '192.168.1.1 and 10.0.0.1'")
        
        # Interactive mode
        while True:
            try:
                ip_input = input("\nEnter IP address (or 'quit' to exit): ").strip()
                if ip_input.lower() in ['quit', 'exit', 'q']:
                    break
                if ip_input:
                    print()
                    format_single_ip(ip_input)
                    print()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    else:
        # Command line argument mode
        ip_input = ' '.join(sys.argv[1:])
        format_single_ip(ip_input)


if __name__ == "__main__":
    main()