#!/usr/bin/env python3
"""C++ 命名规范检查工具"""

import sys
import json
import re
from pathlib import Path

# 命名规范数据
NAMING_RULES = {
    "variable": {
        "style": "snake_case",
        "description": "变量名使用小写字母和下划线",
        "patterns": {
            "good": r"^[a-z][a-z0-9_]*$",
            "bad": r"^[A-Z]|[A-Z][a-z]|^[a-z]+[A-Z]"
        },
        "examples": {
            "good": ["user_name", "total_count", "max_value"],
            "bad": ["userName", "TotalCount", "MAXVALUE"]
        },
        "rules": [
            "使用描述性名称，避免单字母变量（除了循环计数器）",
            "布尔变量使用 is_、has_、can_ 等前缀",
            "避免使用缩写，除非是广为人知的（如 id、url）"
        ]
    },
    "constant": {
        "style": "UPPER_SNAKE_CASE 或 kCamelCase",
        "description": "常量使用全大写下划线或 k 前缀驼峰命名",
        "patterns": {
            "good": r"^[A-Z][A-Z0-9_]*$|^k[A-Z][a-zA-Z0-9]*$",
            "bad": r"^[a-z]"
        },
        "examples": {
            "good": ["MAX_BUFFER_SIZE", "kDefaultTimeout", "PI"],
            "bad": ["maxBufferSize", "max_buffer_size", "default_timeout"]
        },
        "rules": [
            "宏定义使用 UPPER_SNAKE_CASE",
            "constexpr 和 const 变量可使用 kCamelCase（Google Style）",
            "枚举值使用 kCamelCase 或 UPPER_SNAKE_CASE"
        ]
    },
    "function": {
        "style": "snake_case 或 CamelCase",
        "description": "函数名使用小写下划线或大驼峰",
        "patterns": {
            "good": r"^[a-z][a-z0-9_]*$|^[A-Z][a-zA-Z0-9]*$",
            "bad": r"^[A-Z][a-z]+_[a-z]"
        },
        "examples": {
            "good": ["calculate_total", "CalculateTotal", "get_user_name"],
            "bad": ["Calculate_Total", "calculatetotal", "CALCULATE_TOTAL"]
        },
        "rules": [
            "使用动词或动词短语",
            "getter 函数可以省略 get_ 前缀（如 name() 而非 get_name()）",
            "setter 函数使用 set_ 前缀",
            "布尔返回值函数使用 is_、has_、can_ 等前缀"
        ]
    },
    "class": {
        "style": "PascalCase",
        "description": "类名使用大驼峰命名",
        "patterns": {
            "good": r"^[A-Z][a-zA-Z0-9]*$",
            "bad": r"^[a-z]|^[a-z]+_[a-z]"
        },
        "examples": {
            "good": ["UserManager", "HttpClient", "DatabaseConnection"],
            "bad": ["userManager", "HTTPClient", "database_connection"]
        },
        "rules": [
            "使用名词或名词短语",
            "接口类可以使用 I 前缀（如 ILogger）或 Interface 后缀",
            "抽象类可以使用 Abstract 前缀或 Base 前缀",
            "避免使用 Manager、Handler 等模糊后缀，除非确实合适"
        ]
    },
    "namespace": {
        "style": "snake_case 或 lowercase",
        "description": "命名空间使用小写或小写下划线",
        "patterns": {
            "good": r"^[a-z][a-z0-9_]*$",
            "bad": r"^[A-Z]"
        },
        "examples": {
            "good": ["utils", "http_client", "database"],
            "bad": ["Utils", "HttpClient", "DATA_BASE"]
        },
        "rules": [
            "使用简短、描述性的名称",
            "避免嵌套过深（建议不超过 3 层）",
            "不要使用 using namespace 在头文件中"
        ]
    },
    "member_variable": {
        "style": "suffix with _ 或 m_ prefix",
        "description": "成员变量使用下划线后缀或 m_ 前缀",
        "patterns": {
            "good": r"^[a-z][a-z0-9_]*_$|^m_[a-z][a-z0-9_]*$",
            "bad": r"^[a-z][a-zA-Z0-9]*$|^_[a-z]"
        },
        "examples": {
            "good": ["name_", "m_name", "count_", "m_count"],
            "bad": ["name", "mName", "_name"]
        },
        "rules": [
            "私有成员变量使用下划线后缀（Google Style）",
            "或使用 m_ 前缀（Hungarian notation）",
            "公有成员变量不推荐，考虑使用 getter/setter",
            "静态成员变量可使用 s_ 前缀"
        ]
    },
    "template_parameter": {
        "style": "PascalCase 或 single uppercase",
        "description": "模板参数使用大驼峰或单个大写字母",
        "patterns": {
            "good": r"^[A-Z]$|^[A-Z][a-zA-Z0-9]*$",
            "bad": r"^[a-z]"
        },
        "examples": {
            "good": ["T", "TKey", "TValue", "Container"],
            "bad": ["t", "tKey", "container"]
        },
        "rules": [
            "单个类型参数使用 T",
            "多个参数使用描述性名称（TKey, TValue）",
            "概念（Concepts）使用大驼峰命名"
        ]
    },
    "file_naming": {
        "style": "snake_case.cpp 或 PascalCase.cpp",
        "description": "文件名使用小写下划线或大驼峰",
        "patterns": {
            "good": r"^[a-z][a-z0-9_]*\.([ch]|cpp|hpp|cc)$|^[A-Z][a-zA-Z0-9]*\.([ch]|cpp|hpp|cc)$",
            "bad": r"[A-Z][a-z]+_[a-z]|\.CPP|\.H"
        },
        "examples": {
            "good": ["user_manager.cpp", "UserManager.cpp", "http_client.h"],
            "bad": ["UserManager.CPP", "user-manager.cpp", "HTTPLIENT.h"]
        },
        "rules": [
            "头文件使用 .h 或 .hpp",
            "实现文件使用 .cpp 或 .cc",
            "文件名应与主要类名匹配",
            "测试文件添加 _test 后缀"
        ]
    }
}


def check_naming(identifier: str, category: str) -> tuple[bool, str, list[str]]:
    """检查命名是否符合规范"""
    if category not in NAMING_RULES:
        return False, f"未知的类别: {category}", []

    rule = NAMING_RULES[category]
    pattern = re.compile(rule["patterns"]["good"])

    is_valid = bool(pattern.match(identifier))

    details = f"类别: {category}\n"
    details += f"期望风格: {rule['style']}\n"
    details += f"检查结果: {'✅ 符合规范' if is_valid else '❌ 不符合规范'}\n"

    if not is_valid:
        details += f"\n符合规范的示例:\n"
        for ex in rule["examples"]["good"][:3]:
            details += f"  - {ex}\n"

    return is_valid, details, rule["examples"]["good"]


def main():
    if len(sys.argv) != 3:
        print("用法: naming_checker.py <identifier> <category>")
        print("\n可用类别:")
        for cat in NAMING_RULES:
            print(f"  - {cat}")
        sys.exit(1)

    identifier = sys.argv[1]
    category = sys.argv[2]

    is_valid, details, suggestions = check_naming(identifier, category)

    print(details)

    if suggestions and not is_valid:
        print("\n推荐使用:")
        for sug in suggestions[:3]:
            print(f"  • {sug}")


if __name__ == "__main__":
    main()
