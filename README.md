# IP Address Formatter

一个功能完整的IP地址格式化、验证和转换工具集。支持IPv4和IPv6地址的各种操作。

## 功能特性

- ✅ **IP地址验证**: 支持IPv4和IPv6地址格式验证
- ✅ **地址标准化**: 移除前导零，统一格式
- ✅ **文本提取**: 从文本中提取所有有效的IP地址
- ✅ **网络信息**: 获取网络地址、广播地址、子网掩码等信息
- ✅ **格式转换**: IPv4与整数间的相互转换
- ✅ **CIDR支持**: 支持CIDR记法和子网掩码
- ✅ **命令行工具**: 提供易用的CLI接口

## 文件说明

- `ip_formatter.py` - 核心IP格式化类库
- `format_ip.py` - 命令行工具
- `usage_examples.py` - 使用示例和演示

## 快速开始

### 使用Python库

```python
from ip_formatter import IPFormatter

formatter = IPFormatter()

# 验证IP地址
print(formatter.is_valid_ip("192.168.1.1"))  # True
print(formatter.is_valid_ip("192.168.001.001"))  # True

# 标准化IP地址
print(formatter.normalize_ip("192.168.001.001"))  # "192.168.1.1"

# 从文本提取IP
text = "服务器日志显示来自 192.168.001.100 和 10.0.0.5 的连接"
ips = formatter.extract_ips_from_text(text)
print(ips)  # ['192.168.001.100', '10.0.0.5']
```

### 使用命令行工具

```bash
# 验证IP地址
python3 format_ip.py validate 192.168.1.1

# 标准化IP地址
python3 format_ip.py normalize "192.168.001.001"

# 从文本提取IP
python3 format_ip.py extract "服务器在 192.168.1.1 和 10.0.0.1" --normalize

# 获取网络信息
python3 format_ip.py network 192.168.1.100 24

# IPv4转整数
python3 format_ip.py convert-to-int 192.168.1.1

# 整数转IPv4
python3 format_ip.py convert-from-int 3232235777
```

## 支持的IP格式

### IPv4
- 标准格式: `192.168.1.1`
- 带前导零: `192.168.001.001`
- 私有地址: `10.0.0.1`, `172.16.0.1`, `192.168.1.1`
- 公网地址: `8.8.8.8`, `1.1.1.1`

### IPv6
- 标准格式: `2001:db8:85a3::8a2e:370:7334`
- 完整格式: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- 本地地址: `::1`, `::`

## 运行示例

```bash
# 运行完整演示
python3 ip_formatter.py

# 运行使用示例
python3 usage_examples.py

# 查看CLI帮助
python3 format_ip.py --help
```

## 主要功能

1. **地址验证**: 准确识别有效的IPv4和IPv6地址
2. **格式标准化**: 统一IP地址格式，移除不必要的前导零
3. **网络计算**: 计算网络地址、广播地址、可用地址数等
4. **批量处理**: 支持批量验证和格式化IP地址列表
5. **文本解析**: 智能从各种文本格式中提取IP地址
6. **多种输出**: 支持标准格式、整数格式、二进制格式等

这个工具集可以满足各种IP地址处理需求，适用于网络管理、日志分析、配置文件处理等场景。