#!/usr/bin/env python3
"""
IP Address Formatter
====================
A comprehensive utility for IP address validation, formatting, and conversion.
Supports both IPv4 and IPv6 addresses with various formatting options.
"""

import re
import ipaddress
from typing import Union, List, Optional, Tuple


class IPFormatter:
    """IP address formatter with validation and conversion capabilities."""
    
    def __init__(self):
        # IPv4 regex pattern
        self.ipv4_pattern = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        
        # IPv6 regex pattern (simplified)
        self.ipv6_pattern = re.compile(
            r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|'
            r'^::1$|^::$|'
            r'^(?:[0-9a-fA-F]{1,4}:)*::(?:[0-9a-fA-F]{1,4}:)*[0-9a-fA-F]{1,4}$'
        )
    
    def is_valid_ipv4(self, ip: str) -> bool:
        """Validate IPv4 address format."""
        try:
            # Use regex pattern for validation that allows leading zeros
            ip_clean = ip.strip()
            if not self.ipv4_pattern.match(ip_clean):
                return False
            
            # Additional validation: check each octet is in valid range
            octets = ip_clean.split('.')
            for octet in octets:
                if int(octet) > 255:
                    return False
            
            return True
        except (ValueError, AttributeError):
            return False
    
    def is_valid_ipv6(self, ip: str) -> bool:
        """Validate IPv6 address format."""
        try:
            ipaddress.IPv6Address(ip.strip())
            return True
        except ipaddress.AddressValueError:
            return False
    
    def is_valid_ip(self, ip: str) -> bool:
        """Validate if string is a valid IP address (IPv4 or IPv6)."""
        return self.is_valid_ipv4(ip) or self.is_valid_ipv6(ip)
    
    def get_ip_version(self, ip: str) -> Optional[int]:
        """Get IP version (4 or 6) or None if invalid."""
        if self.is_valid_ipv4(ip):
            return 4
        elif self.is_valid_ipv6(ip):
            return 6
        return None
    
    def normalize_ipv4(self, ip: str) -> str:
        """Normalize IPv4 address (remove leading zeros, etc.)."""
        if not self.is_valid_ipv4(ip):
            raise ValueError(f"Invalid IPv4 address: {ip}")
        
        # Handle leading zeros by parsing each octet
        ip_clean = ip.strip()
        octets = ip_clean.split('.')
        normalized_octets = [str(int(octet)) for octet in octets]
        normalized_ip = '.'.join(normalized_octets)
        
        return normalized_ip
    
    def normalize_ipv6(self, ip: str) -> str:
        """Normalize IPv6 address (compress zeros, lowercase, etc.)."""
        if not self.is_valid_ipv6(ip):
            raise ValueError(f"Invalid IPv6 address: {ip}")
        
        return str(ipaddress.IPv6Address(ip.strip()))
    
    def normalize_ip(self, ip: str) -> str:
        """Normalize IP address (IPv4 or IPv6)."""
        ip = ip.strip()
        if self.is_valid_ipv4(ip):
            return self.normalize_ipv4(ip)
        elif self.is_valid_ipv6(ip):
            return self.normalize_ipv6(ip)
        else:
            raise ValueError(f"Invalid IP address: {ip}")
    
    def format_ipv4_with_mask(self, ip: str, mask: Union[str, int]) -> str:
        """Format IPv4 address with subnet mask or CIDR notation."""
        if not self.is_valid_ipv4(ip):
            raise ValueError(f"Invalid IPv4 address: {ip}")
        
        normalized_ip = self.normalize_ipv4(ip)
        
        if isinstance(mask, str):
            if self.is_valid_ipv4(mask):
                # Normalize mask as well
                normalized_mask = self.normalize_ipv4(mask)
                # Convert subnet mask to CIDR
                network = ipaddress.IPv4Network(f"{normalized_ip}/{normalized_mask}", strict=False)
                return f"{normalized_ip}/{network.prefixlen}"
            else:
                raise ValueError(f"Invalid subnet mask: {mask}")
        elif isinstance(mask, int):
            if 0 <= mask <= 32:
                return f"{normalized_ip}/{mask}"
            else:
                raise ValueError(f"Invalid CIDR prefix: {mask}")
        else:
            raise ValueError("Mask must be string (subnet mask) or int (CIDR)")
    
    def format_ipv6_with_prefix(self, ip: str, prefix: int) -> str:
        """Format IPv6 address with prefix length."""
        if not self.is_valid_ipv6(ip):
            raise ValueError(f"Invalid IPv6 address: {ip}")
        
        if not (0 <= prefix <= 128):
            raise ValueError(f"Invalid IPv6 prefix length: {prefix}")
        
        normalized_ip = self.normalize_ipv6(ip)
        return f"{normalized_ip}/{prefix}"
    
    def extract_ips_from_text(self, text: str) -> List[str]:
        """Extract all valid IP addresses from text."""
        ips = []
        
        # Find potential IPv4 addresses
        ipv4_candidates = re.findall(
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            text
        )
        
        for candidate in ipv4_candidates:
            if self.is_valid_ipv4(candidate):
                ips.append(candidate)
        
        # Find potential IPv6 addresses (simplified pattern)
        ipv6_candidates = re.findall(
            r'\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b|'
            r'\b::1\b|\b::\b',
            text
        )
        
        for candidate in ipv6_candidates:
            if self.is_valid_ipv6(candidate):
                ips.append(candidate)
        
        return ips
    
    def format_ip_list(self, ip_list: List[str], normalize: bool = True) -> List[str]:
        """Format a list of IP addresses."""
        formatted_ips = []
        
        for ip in ip_list:
            try:
                if normalize:
                    formatted_ips.append(self.normalize_ip(ip))
                else:
                    if self.is_valid_ip(ip):
                        formatted_ips.append(ip.strip())
            except ValueError:
                # Skip invalid IPs
                continue
        
        return formatted_ips
    
    def convert_ipv4_to_int(self, ip: str) -> int:
        """Convert IPv4 address to integer representation."""
        if not self.is_valid_ipv4(ip):
            raise ValueError(f"Invalid IPv4 address: {ip}")
        
        # Normalize first to handle leading zeros
        normalized_ip = self.normalize_ipv4(ip)
        return int(ipaddress.IPv4Address(normalized_ip))
    
    def convert_int_to_ipv4(self, ip_int: int) -> str:
        """Convert integer to IPv4 address."""
        if not (0 <= ip_int <= 4294967295):  # 2^32 - 1
            raise ValueError(f"Invalid IPv4 integer: {ip_int}")
        
        return str(ipaddress.IPv4Address(ip_int))
    
    def get_network_info(self, ip: str, mask: Union[str, int]) -> dict:
        """Get network information for an IP address with mask/prefix."""
        try:
            if self.is_valid_ipv4(ip):
                normalized_ip = self.normalize_ipv4(ip)
                if isinstance(mask, str) and self.is_valid_ipv4(mask):
                    normalized_mask = self.normalize_ipv4(mask)
                    network = ipaddress.IPv4Network(f"{normalized_ip}/{normalized_mask}", strict=False)
                elif isinstance(mask, int):
                    network = ipaddress.IPv4Network(f"{normalized_ip}/{mask}", strict=False)
                else:
                    raise ValueError("Invalid mask format")
            elif self.is_valid_ipv6(ip):
                normalized_ip = self.normalize_ipv6(ip)
                if isinstance(mask, int):
                    network = ipaddress.IPv6Network(f"{normalized_ip}/{mask}", strict=False)
                else:
                    raise ValueError("IPv6 requires integer prefix length")
            else:
                raise ValueError("Invalid IP address")
            
            return {
                'network_address': str(network.network_address),
                'broadcast_address': str(network.broadcast_address) if hasattr(network, 'broadcast_address') else None,
                'netmask': str(network.netmask),
                'prefix_length': network.prefixlen,
                'num_addresses': network.num_addresses,
                'is_private': network.is_private,
                'is_multicast': network.is_multicast,
                'is_reserved': network.is_reserved
            }
        
        except Exception as e:
            raise ValueError(f"Error getting network info: {str(e)}")


def main():
    """Example usage of the IP formatter."""
    formatter = IPFormatter()
    
    # Test cases
    test_ips = [
        "192.168.1.1",
        "192.168.001.001",
        "10.0.0.1",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:85a3::8a2e:370:7334",
        "::1",
        "invalid.ip.address",
        "256.256.256.256"
    ]
    
    print("IP Address Validation and Formatting")
    print("=" * 40)
    
    for ip in test_ips:
        print(f"\nTesting: {ip}")
        print(f"  Valid: {formatter.is_valid_ip(ip)}")
        
        if formatter.is_valid_ip(ip):
            version = formatter.get_ip_version(ip)
            print(f"  Version: IPv{version}")
            
            try:
                normalized = formatter.normalize_ip(ip)
                print(f"  Normalized: {normalized}")
                
                if version == 4:
                    ip_int = formatter.convert_ipv4_to_int(normalized)
                    print(f"  As integer: {ip_int}")
                    
                    # Network info example
                    try:
                        net_info = formatter.get_network_info(normalized, 24)
                        print(f"  Network (/24): {net_info['network_address']}")
                        print(f"  Broadcast: {net_info['broadcast_address']}")
                        print(f"  Is private: {net_info['is_private']}")
                    except:
                        pass
                        
            except ValueError as e:
                print(f"  Error: {e}")
    
    # Text extraction example
    sample_text = """
    Server logs show connections from 192.168.1.100, 10.0.0.5, and 2001:db8::1.
    Invalid entries like 999.999.999.999 should be ignored.
    Also found 172.16.0.1 and ::1 in the data.
    """
    
    print("\n\nIP Extraction from Text")
    print("=" * 25)
    print("Sample text:", sample_text.strip())
    
    extracted_ips = formatter.extract_ips_from_text(sample_text)
    print(f"\nExtracted IPs: {extracted_ips}")
    
    normalized_ips = formatter.format_ip_list(extracted_ips)
    print(f"Normalized IPs: {normalized_ips}")


if __name__ == "__main__":
    main()