#!/usr/bin/env python3
"""
Command-line IP Address Formatter
=================================
Simple CLI tool for formatting and validating IP addresses.
"""

import sys
import argparse
from ip_formatter import IPFormatter


def main():
    parser = argparse.ArgumentParser(
        description='Format and validate IP addresses',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s validate 192.168.1.1
  %(prog)s normalize "192.168.001.001"
  %(prog)s extract "Server at 192.168.1.1 and 10.0.0.1"
  %(prog)s network 192.168.1.100 24
  %(prog)s convert-to-int 192.168.1.1
  %(prog)s convert-from-int 3232235777
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate IP address')
    validate_parser.add_argument('ip', help='IP address to validate')
    
    # Normalize command
    normalize_parser = subparsers.add_parser('normalize', help='Normalize IP address')
    normalize_parser.add_argument('ip', help='IP address to normalize')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract IPs from text')
    extract_parser.add_argument('text', help='Text to extract IPs from')
    extract_parser.add_argument('--normalize', action='store_true', help='Normalize extracted IPs')
    
    # Network info command
    network_parser = subparsers.add_parser('network', help='Get network information')
    network_parser.add_argument('ip', help='IP address')
    network_parser.add_argument('mask', help='Subnet mask (IPv4) or prefix length (IPv6)')
    
    # Convert to integer command
    to_int_parser = subparsers.add_parser('convert-to-int', help='Convert IPv4 to integer')
    to_int_parser.add_argument('ip', help='IPv4 address to convert')
    
    # Convert from integer command
    from_int_parser = subparsers.add_parser('convert-from-int', help='Convert integer to IPv4')
    from_int_parser.add_argument('integer', type=int, help='Integer to convert to IPv4')
    
    # Format with mask command
    format_parser = subparsers.add_parser('format-with-mask', help='Format IP with mask/prefix')
    format_parser.add_argument('ip', help='IP address')
    format_parser.add_argument('mask', help='Subnet mask or CIDR prefix')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    formatter = IPFormatter()
    
    try:
        if args.command == 'validate':
            is_valid = formatter.is_valid_ip(args.ip)
            version = formatter.get_ip_version(args.ip)
            print(f"IP: {args.ip}")
            print(f"Valid: {is_valid}")
            if is_valid:
                print(f"Version: IPv{version}")
        
        elif args.command == 'normalize':
            normalized = formatter.normalize_ip(args.ip)
            print(f"Original: {args.ip}")
            print(f"Normalized: {normalized}")
        
        elif args.command == 'extract':
            extracted = formatter.extract_ips_from_text(args.text)
            print(f"Text: {args.text}")
            print(f"Extracted IPs: {extracted}")
            
            if args.normalize and extracted:
                normalized = formatter.format_ip_list(extracted, normalize=True)
                print(f"Normalized: {normalized}")
        
        elif args.command == 'network':
            try:
                # Try to convert mask to int for CIDR notation
                mask = int(args.mask)
            except ValueError:
                # Keep as string for subnet mask
                mask = args.mask
            
            network_info = formatter.get_network_info(args.ip, mask)
            print(f"IP: {args.ip}")
            print(f"Mask/Prefix: {args.mask}")
            print(f"Network: {network_info['network_address']}")
            if network_info['broadcast_address']:
                print(f"Broadcast: {network_info['broadcast_address']}")
            print(f"Netmask: {network_info['netmask']}")
            print(f"Prefix Length: {network_info['prefix_length']}")
            print(f"Total Addresses: {network_info['num_addresses']}")
            print(f"Private: {network_info['is_private']}")
            print(f"Multicast: {network_info['is_multicast']}")
            print(f"Reserved: {network_info['is_reserved']}")
        
        elif args.command == 'convert-to-int':
            ip_int = formatter.convert_ipv4_to_int(args.ip)
            print(f"IPv4: {args.ip}")
            print(f"Integer: {ip_int}")
            print(f"Hex: 0x{ip_int:08x}")
            print(f"Binary: {bin(ip_int)}")
        
        elif args.command == 'convert-from-int':
            ip = formatter.convert_int_to_ipv4(args.integer)
            print(f"Integer: {args.integer}")
            print(f"IPv4: {ip}")
        
        elif args.command == 'format-with-mask':
            try:
                # Try to convert mask to int for CIDR notation
                mask = int(args.mask)
            except ValueError:
                # Keep as string for subnet mask
                mask = args.mask
            
            if formatter.is_valid_ipv4(args.ip):
                formatted = formatter.format_ipv4_with_mask(args.ip, mask)
            elif formatter.is_valid_ipv6(args.ip) and isinstance(mask, int):
                formatted = formatter.format_ipv6_with_prefix(args.ip, mask)
            else:
                raise ValueError("Invalid IP or mask combination")
            
            print(f"Formatted: {formatted}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()