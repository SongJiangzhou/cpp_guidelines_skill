#!/usr/bin/env python3
"""C++ 头文件包含保护检查工具"""

import sys
import re
import os


def check_include_guard(code: str, file_path: str = None) -> tuple[bool, str, list[str]]:
    """检查头文件的包含保护是否正确"""
    suggestions = []

    # 检查是否使用了 #pragma once
    has_pragma_once = bool(re.search(r'#pragma\s+once', code))

    # 检查传统的 ifndef 保护
    ifndef_pattern = re.compile(r'#ifndef\s+([A-Z_][A-Z0-9_]*)')
    define_pattern = re.compile(r'#define\s+([A-Z_][A-Z0-9_]*)')
    endif_pattern = re.compile(r'#endif\s*(?://\s*([A-Z_][A-Z0-9_]*))?')

    ifndef_match = ifndef_pattern.search(code)
    define_match = define_pattern.search(code)
    endif_match = endif_pattern.search(code)

    has_traditional_guard = bool(ifndef_match and define_match)

    details = ""

    if has_pragma_once:
        details += "✅ 使用了 #pragma once\n"
    elif has_traditional_guard:
        details += "✅ 使用了传统的 ifndef 保护\n"
        ifndef_name = ifndef_match.group(1)
        define_name = define_match.group(1)
        details += f"   保护宏名: {ifndef_name}\n"

        # 检查 ifndef 和 define 的名称是否匹配
        if ifndef_name != define_name:
            details += f"❌ ifndef 和 define 名称不匹配！\n"
            suggestions.append(f"将 #define {define_name} 改为 #define {ifndef_name}")
            has_traditional_guard = False
        else:
            # 检查 #endif 注释
            if endif_match and endif_match.group(1):
                endif_name = endif_match.group(1)
                if endif_name != ifndef_name:
                    details += f"⚠️ #endif 注释与保护宏名不匹配\n"
    else:
        details += "❌ 未找到包含保护\n"
        # 生成建议的保护宏名
        if file_path:
            base_name = os.path.basename(file_path)
            name_without_ext = os.path.splitext(base_name)[0]
            suggested_name = name_without_ext.upper().replace("-", "_").replace(".", "_")
        else:
            suggested_name = "HEADER_NAME_H"

        suggestions.append(f"#ifndef {suggested_name}")
        suggestions.append(f"#define {suggested_name}")
        suggestions.append(f"...\n#endif // {suggested_name}")

        return False, details, suggestions

    # 检查保护宏的命名风格
    if has_traditional_guard and ifndef_match:
        guard_name = ifndef_match.group(1)
        if not guard_name.endswith("_H") and not guard_name.endswith("_HPP"):
            details += f"\n⚠️ 建议保护宏名以 _H 或 _HPP 结尾\n"

    is_valid = has_pragma_once or has_traditional_guard
    return is_valid, details, suggestions


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"文件不存在: {file_path}")
            sys.exit(1)
    else:
        # 从 stdin 读取
        code = sys.stdin.read()

    file_path = sys.argv[1] if len(sys.argv) > 1 else ""

    is_valid, details, suggestions = check_include_guard(code, file_path)

    print(details)

    if suggestions and not is_valid:
        print("\n建议的包含保护:")
        for sug in suggestions:
            print(sug)


if __name__ == "__main__":
    main()
