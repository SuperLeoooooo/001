#!/usr/bin/env python3
"""
IP Formatter Usage Examples
===========================
This file demonstrates various ways to use the IP formatter.
"""

from ip_formatter import IPFormatter

def main():
    # Create an instance of the formatter
    formatter = IPFormatter()
    
    print("=== IP Address Validation Examples ===")
    
    # Test various IP formats
    test_cases = [
        "192.168.1.1",           # Standard IPv4
        "192.168.001.001",       # IPv4 with leading zeros
        "10.0.0.1",              # Private IPv4
        "172.16.255.255",        # Private IPv4
        "8.8.8.8",               # Public IPv4
        "2001:db8::1",           # IPv6
        "::1",                   # IPv6 localhost
        "invalid.ip",            # Invalid
        "999.999.999.999",       # Invalid IPv4
    ]
    
    for ip in test_cases:
        is_valid = formatter.is_valid_ip(ip)
        version = formatter.get_ip_version(ip) if is_valid else None
        print(f"{ip:20} -> Valid: {is_valid:5} Version: {version}")
    
    print("\n=== IP Address Normalization Examples ===")
    
    # Normalize IPs with various formats
    normalize_cases = [
        "192.168.001.001",
        "010.000.000.001",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:85a3::8a2e:370:7334",
    ]
    
    for ip in normalize_cases:
        try:
            normalized = formatter.normalize_ip(ip)
            print(f"{ip:35} -> {normalized}")
        except ValueError as e:
            print(f"{ip:35} -> Error: {e}")
    
    print("\n=== Network Information Examples ===")
    
    # Get network information
    network_cases = [
        ("192.168.1.100", 24),
        ("192.168.1.100", "255.255.255.0"),
        ("10.0.0.1", 8),
        ("172.16.0.1", 16),
        ("2001:db8::1", 64),
    ]
    
    for ip, mask in network_cases:
        try:
            info = formatter.get_network_info(ip, mask)
            print(f"\nIP: {ip}, Mask: {mask}")
            print(f"  Network: {info['network_address']}")
            print(f"  Prefix: /{info['prefix_length']}")
            print(f"  Addresses: {info['num_addresses']}")
            print(f"  Private: {info['is_private']}")
        except ValueError as e:
            print(f"Error for {ip}/{mask}: {e}")
    
    print("\n=== IP Conversion Examples ===")
    
    # Convert IPv4 to integer and back
    ipv4_examples = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    
    for ip in ipv4_examples:
        try:
            ip_int = formatter.convert_ipv4_to_int(ip)
            back_to_ip = formatter.convert_int_to_ipv4(ip_int)
            print(f"{ip:15} -> {ip_int:10} -> {back_to_ip}")
        except ValueError as e:
            print(f"Error converting {ip}: {e}")
    
    print("\n=== Text Extraction Examples ===")
    
    # Extract IPs from various text formats
    text_examples = [
        "Server logs: 192.168.1.1, 10.0.0.5 connected",
        "配置文件包含 192.168.001.100 和 172.16.0.1",
        "IPv6 addresses: 2001:db8::1, ::1, fe80::1",
        "Mixed: 192.168.1.1, 2001:db8::1, invalid.ip, 999.999.999.999",
        "Log entry: [2023-01-01] 203.0.113.1 -> 192.168.1.100:80",
    ]
    
    for text in text_examples:
        extracted = formatter.extract_ips_from_text(text)
        normalized = formatter.format_ip_list(extracted, normalize=True)
        print(f"\nText: {text}")
        print(f"Extracted: {extracted}")
        print(f"Normalized: {normalized}")
    
    print("\n=== CIDR and Subnet Mask Examples ===")
    
    # Format IPs with various mask formats
    cidr_examples = [
        ("192.168.1.100", 24),
        ("192.168.1.100", "255.255.255.0"),
        ("10.0.0.1", 8),
        ("172.16.0.1", "255.255.0.0"),
        ("2001:db8::1", 64),
    ]
    
    for ip, mask in cidr_examples:
        try:
            if formatter.is_valid_ipv4(ip):
                formatted = formatter.format_ipv4_with_mask(ip, mask)
            elif formatter.is_valid_ipv6(ip) and isinstance(mask, int):
                formatted = formatter.format_ipv6_with_prefix(ip, mask)
            else:
                formatted = "Invalid combination"
            
            print(f"{ip:15} + {str(mask):15} -> {formatted}")
        except ValueError as e:
            print(f"Error: {e}")
    
    print("\n=== Batch Processing Example ===")
    
    # Process a list of mixed IPs
    mixed_ips = [
        "192.168.001.001",
        "10.0.0.1",
        "invalid.ip",
        "2001:db8::1",
        "172.16.255.255",
        "999.999.999.999",
        "::1",
        "8.8.8.8"
    ]
    
    print("Original IPs:", mixed_ips)
    
    # Filter and normalize valid IPs
    valid_ips = [ip for ip in mixed_ips if formatter.is_valid_ip(ip)]
    print("Valid IPs:", valid_ips)
    
    normalized_ips = formatter.format_ip_list(valid_ips, normalize=True)
    print("Normalized:", normalized_ips)
    
    # Separate by version
    ipv4_list = [ip for ip in normalized_ips if formatter.get_ip_version(ip) == 4]
    ipv6_list = [ip for ip in normalized_ips if formatter.get_ip_version(ip) == 6]
    
    print("IPv4 addresses:", ipv4_list)
    print("IPv6 addresses:", ipv6_list)

if __name__ == "__main__":
    main()