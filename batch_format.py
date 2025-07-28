#!/usr/bin/env python3
"""
Batch IP formatter for processing multiple IP addresses.
Usage: python batch_format.py input.txt [output.txt]
"""

import sys
from ip_formatter import IPFormatter


def process_file(input_file: str, output_file: str = None):
    """Process IP addresses from a file."""
    formatter = IPFormatter()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
        return
    except Exception as e:
        print(f"错误：读取文件时出错 - {e}")
        return
    
    # Extract all IPs from the file
    extracted_ips = formatter.extract_ips_from_text(content)
    
    if not extracted_ips:
        print("文件中没有找到有效的IP地址")
        return
    
    results = []
    results.append("IP地址格式化结果")
    results.append("=" * 50)
    results.append(f"输入文件: {input_file}")
    results.append(f"找到IP地址数量: {len(extracted_ips)}")
    results.append("")
    
    for i, ip in enumerate(extracted_ips, 1):
        results.append(f"{i}. 原始IP: {ip}")
        
        if formatter.is_valid_ipv4(ip):
            normalized = formatter.normalize_ipv4(ip)
            results.append(f"   类型: IPv4")
            results.append(f"   标准化: {normalized}")
            
            # Add common CIDR formats
            for mask in [24, 16, 8]:
                cidr = formatter.format_ip_with_mask(normalized, mask)
                if cidr:
                    results.append(f"   /{mask}: {cidr}")
                    
        elif formatter.is_valid_ipv6(ip):
            normalized = formatter.normalize_ipv6(ip)
            expanded = formatter.expand_ipv6(ip)
            compressed = formatter.compress_ipv6(ip)
            
            results.append(f"   类型: IPv6")
            results.append(f"   标准化: {normalized}")
            results.append(f"   展开: {expanded}")
            results.append(f"   压缩: {compressed}")
        
        results.append("")
    
    # Create summary
    ipv4_count = sum(1 for ip in extracted_ips if formatter.is_valid_ipv4(ip))
    ipv6_count = sum(1 for ip in extracted_ips if formatter.is_valid_ipv6(ip))
    
    results.append("统计信息:")
    results.append(f"- IPv4地址: {ipv4_count}")
    results.append(f"- IPv6地址: {ipv6_count}")
    results.append(f"- 总计: {len(extracted_ips)}")
    
    # Output results
    output_text = '\n'.join(results)
    
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"结果已保存到: {output_file}")
        except Exception as e:
            print(f"错误：保存文件时出错 - {e}")
            print("\n结果:")
            print(output_text)
    else:
        print(output_text)


def create_sample_file():
    """Create a sample input file for testing."""
    sample_content = """
网络配置文件示例

服务器配置:
- Web服务器: 192.168.001.100
- 数据库服务器: 192.168.001.200  
- 缓存服务器: 10.000.000.050

IPv6服务器:
- 主服务器: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
- 备份服务器: 2001:db8:85a3::8a2e:370:7335
- 本地服务器: ::1

日志记录:
访问来自 172.016.254.001, 192.168.1.1, 和一些无效的地址如 999.999.999.999
"""
    
    with open('sample_ips.txt', 'w', encoding='utf-8') as f:
        f.write(sample_content.strip())
    
    print("已创建示例文件: sample_ips.txt")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("IP地址批量格式化工具")
        print("使用方法: python batch_format.py input.txt [output.txt]")
        print("\n选项:")
        print("  --create-sample  创建示例输入文件")
        print("\n示例:")
        print("  python batch_format.py sample_ips.txt")
        print("  python batch_format.py input.txt formatted_output.txt")
        return
    
    if sys.argv[1] == '--create-sample':
        create_sample_file()
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_file(input_file, output_file)


if __name__ == "__main__":
    main()