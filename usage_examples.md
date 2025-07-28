# IP格式化工具使用指南

这个工具可以帮助你格式化和验证IP地址，支持IPv4和IPv6。

## 功能特性

- ✅ IPv4地址验证和格式化
- ✅ IPv6地址验证和格式化  
- ✅ 去除IPv4前导零
- ✅ IPv6地址压缩和展开
- ✅ 从文本中提取IP地址
- ✅ CIDR网络格式化
- ✅ 命令行和交互式使用

## 使用方法

### 1. 命令行使用

```bash
# 格式化单个IPv4地址（去除前导零）
python3 format_ip.py 192.168.001.001

# 格式化IPv6地址
python3 format_ip.py "2001:0db8:85a3:0000:0000:8a2e:0370:7334"

# 从文本中提取IP地址
python3 format_ip.py "服务器日志显示来自192.168.1.100和10.0.0.1的连接"
```

### 2. 交互式使用

```bash
# 启动交互模式
python3 format_ip.py
```

### 3. 在Python代码中使用

```python
from ip_formatter import IPFormatter

formatter = IPFormatter()

# 验证IP地址
print(formatter.is_valid_ipv4("192.168.1.1"))  # True
print(formatter.is_valid_ipv6("2001:db8::1"))  # True

# 格式化IPv4地址（去除前导零）
print(formatter.normalize_ipv4("192.168.001.001"))  # "192.168.1.1"

# 格式化IPv6地址
print(formatter.normalize_ipv6("2001:0db8::0001"))  # "2001:db8::1"
print(formatter.expand_ipv6("2001:db8::1"))        # "2001:0db8:0000:0000:0000:0000:0000:0001"
print(formatter.compress_ipv6("2001:0db8:0000:0000:0000:0000:0000:0001"))  # "2001:db8::1"

# 从文本提取IP地址
text = "服务器192.168.1.100和10.0.0.1正在运行"
ips = formatter.extract_ips_from_text(text)
print(ips)  # ['192.168.1.100', '10.0.0.1']

# CIDR格式化
print(formatter.format_ip_with_mask("192.168.1.1", 24))  # "192.168.1.0/24"
```

## 示例输出

### IPv4地址格式化
```
Input: 192.168.001.001
------------------------------
Type: IPv4
Normalized: 192.168.1.1
Common CIDR formats:
  /24: 192.168.1.0/24
  /16: 192.168.0.0/16
  /8: 192.0.0.0/8
```

### IPv6地址格式化
```
Input: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
------------------------------
Type: IPv6
Normalized: 2001:db8:85a3::8a2e:370:7334
Expanded: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
Compressed: 2001:db8:85a3::8a2e:370:7334
```

## 常见用途

1. **日志分析**: 从日志文件中提取和标准化IP地址
2. **网络配置**: 验证和格式化网络配置中的IP地址
3. **数据清理**: 统一IP地址格式，去除前导零
4. **网络规划**: 生成CIDR格式的网络地址

## 文件说明

- `ip_formatter.py`: 核心IP格式化类和功能
- `format_ip.py`: 简单的命令行工具
- `usage_examples.md`: 使用说明文档