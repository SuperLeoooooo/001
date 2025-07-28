# IP地址格式化工具

一个功能完整的IP地址格式化和验证工具，支持IPv4和IPv6地址的标准化处理。

## 功能特性

- ✅ IPv4地址验证和格式化（去除前导零）
- ✅ IPv6地址验证和格式化（标准化、展开、压缩）
- ✅ 从文本中自动提取IP地址
- ✅ CIDR网络格式化
- ✅ 命令行工具和交互式使用
- ✅ 批量处理多个IP地址

## 快速开始

```bash
# 格式化单个IP地址
python3 format_ip.py 192.168.001.001

# 交互式模式
python3 format_ip.py

# 批量处理文件中的IP地址
python3 batch_format.py --create-sample
python3 batch_format.py sample_ips.txt
```

## 文件说明

- `ip_formatter.py` - 核心IP格式化类库
- `format_ip.py` - 命令行工具
- `batch_format.py` - 批量处理工具
- `usage_examples.md` - 详细使用说明

查看 `usage_examples.md` 了解更多使用方法和示例。