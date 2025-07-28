#!/usr/bin/env python3
"""
IP Address Formatter Utility
Provides various IP address formatting and validation functions.
"""

import re
import ipaddress
from typing import List, Union, Optional


class IPFormatter:
    """IP address formatter with validation and formatting capabilities."""
    
    # IPv4 regex pattern
    IPV4_PATTERN = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    
    # IPv6 regex pattern (simplified)
    IPV6_PATTERN = re.compile(
        r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|'
        r'^::1$|^::$|'
        r'^(?:[0-9a-fA-F]{1,4}:)*::(?:[0-9a-fA-F]{1,4}:)*[0-9a-fA-F]{1,4}$'
    )
    
    @staticmethod
    def is_valid_ipv4(ip: str) -> bool:
        """Check if string is a valid IPv4 address."""
        try:
            # Handle leading zeros by normalizing first
            parts = ip.split('.')
            if len(parts) == 4:
                for part in parts:
                    if not part or int(part) > 255:
                        return False
                normalized_parts = [str(int(part)) for part in parts]
                normalized_ip = '.'.join(normalized_parts)
                ipaddress.IPv4Address(normalized_ip)
                return True
            else:
                ipaddress.IPv4Address(ip)
                return True
        except (ipaddress.AddressValueError, ValueError):
            return False
    
    @staticmethod
    def is_valid_ipv6(ip: str) -> bool:
        """Check if string is a valid IPv6 address."""
        try:
            ipaddress.IPv6Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Check if string is a valid IP address (IPv4 or IPv6)."""
        try:
            ipaddress.ip_address(ip)
            return True
        except ipaddress.AddressValueError:
            return False
    
    @staticmethod
    def normalize_ipv4(ip: str) -> Optional[str]:
        """Normalize IPv4 address (remove leading zeros, validate)."""
        try:
            # Handle leading zeros by parsing each octet
            parts = ip.split('.')
            if len(parts) == 4:
                normalized_parts = []
                for part in parts:
                    # Remove leading zeros but keep single zero
                    normalized_part = str(int(part))
                    normalized_parts.append(normalized_part)
                normalized_ip = '.'.join(normalized_parts)
                return str(ipaddress.IPv4Address(normalized_ip))
            else:
                return str(ipaddress.IPv4Address(ip))
        except (ipaddress.AddressValueError, ValueError):
            return None
    
    @staticmethod
    def normalize_ipv6(ip: str) -> Optional[str]:
        """Normalize IPv6 address (standard format)."""
        try:
            return str(ipaddress.IPv6Address(ip))
        except ipaddress.AddressValueError:
            return None
    
    @staticmethod
    def expand_ipv6(ip: str) -> Optional[str]:
        """Expand IPv6 address to full format."""
        try:
            ipv6 = ipaddress.IPv6Address(ip)
            return ipv6.exploded
        except ipaddress.AddressValueError:
            return None
    
    @staticmethod
    def compress_ipv6(ip: str) -> Optional[str]:
        """Compress IPv6 address to shortest format."""
        try:
            ipv6 = ipaddress.IPv6Address(ip)
            return ipv6.compressed
        except ipaddress.AddressValueError:
            return None
    
    @staticmethod
    def format_ip_with_mask(ip: str, mask: Union[str, int]) -> Optional[str]:
        """Format IP address with subnet mask or CIDR notation."""
        try:
            if isinstance(mask, int):
                network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
            else:
                # Convert subnet mask to CIDR if needed
                if '.' in mask:  # Subnet mask format
                    mask_int = sum(bin(int(x)).count('1') for x in mask.split('.'))
                    network = ipaddress.ip_network(f"{ip}/{mask_int}", strict=False)
                else:
                    network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
            return str(network)
        except (ipaddress.AddressValueError, ValueError):
            return None
    
    @staticmethod
    def extract_ips_from_text(text: str) -> List[str]:
        """Extract all IP addresses from text."""
        ips = []
        
        # Find IPv4 addresses
        ipv4_matches = re.findall(
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            text
        )
        
        # Validate and add IPv4 addresses
        for ip in ipv4_matches:
            if IPFormatter.is_valid_ipv4(ip):
                ips.append(ip)
        
        # Find IPv6 addresses (basic pattern)
        ipv6_matches = re.findall(
            r'\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b|'
            r'\b::1\b|\b::\b',
            text
        )
        
        # Validate and add IPv6 addresses
        for ip in ipv6_matches:
            if IPFormatter.is_valid_ipv6(ip):
                ips.append(ip)
        
        return list(set(ips))  # Remove duplicates
    
    @staticmethod
    def format_ip_list(ips: List[str], format_type: str = 'normalized') -> List[str]:
        """Format a list of IP addresses."""
        formatted = []
        
        for ip in ips:
            if format_type == 'normalized':
                if IPFormatter.is_valid_ipv4(ip):
                    normalized = IPFormatter.normalize_ipv4(ip)
                    if normalized:
                        formatted.append(normalized)
                elif IPFormatter.is_valid_ipv6(ip):
                    normalized = IPFormatter.normalize_ipv6(ip)
                    if normalized:
                        formatted.append(normalized)
            elif format_type == 'expanded' and IPFormatter.is_valid_ipv6(ip):
                expanded = IPFormatter.expand_ipv6(ip)
                if expanded:
                    formatted.append(expanded)
            elif format_type == 'compressed' and IPFormatter.is_valid_ipv6(ip):
                compressed = IPFormatter.compress_ipv6(ip)
                if compressed:
                    formatted.append(compressed)
            else:
                formatted.append(ip)
        
        return formatted


def main():
    """Example usage of IPFormatter."""
    formatter = IPFormatter()
    
    # Test IP addresses
    test_ips = [
        "192.168.001.001",  # IPv4 with leading zeros
        "10.0.0.1",         # Normal IPv4
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",  # IPv6 full
        "2001:db8:85a3::8a2e:370:7334",             # IPv6 compressed
        "::1",              # IPv6 localhost
        "invalid.ip",       # Invalid IP
    ]
    
    print("IP Address Formatting Examples:")
    print("=" * 50)
    
    for ip in test_ips:
        print(f"\nOriginal: {ip}")
        
        if formatter.is_valid_ipv4(ip):
            print(f"  Type: IPv4")
            print(f"  Normalized: {formatter.normalize_ipv4(ip)}")
        elif formatter.is_valid_ipv6(ip):
            print(f"  Type: IPv6")
            print(f"  Normalized: {formatter.normalize_ipv6(ip)}")
            print(f"  Expanded: {formatter.expand_ipv6(ip)}")
            print(f"  Compressed: {formatter.compress_ipv6(ip)}")
        else:
            print(f"  Status: Invalid IP address")
    
    # Test text extraction
    sample_text = """
    Server logs show connections from 192.168.1.100, 10.0.0.1, and 2001:db8::1.
    Also found 172.16.254.1 and some invalid entries like 999.999.999.999.
    """
    
    print(f"\n\nExtracting IPs from text:")
    print("=" * 50)
    print(f"Text: {sample_text.strip()}")
    extracted = formatter.extract_ips_from_text(sample_text)
    print(f"Extracted IPs: {extracted}")
    print(f"Formatted IPs: {formatter.format_ip_list(extracted)}")


if __name__ == "__main__":
    main()