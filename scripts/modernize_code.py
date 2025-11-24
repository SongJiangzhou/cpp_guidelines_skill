#!/usr/bin/env python3
"""
C++ 代码自动现代化脚本

自动应用常见的现代化转换：
- NULL → nullptr
- typedef → using
- 等等

用法:
    python modernize_code.py <file.cpp> [--dry-run] [--backup]

选项:
    --dry-run    只显示会做的更改，不实际修改文件
    --backup     修改前创建备份文件 (.bak)
"""

import re
import sys
import os
import shutil
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Replacement:
    """替换信息"""
    line_num: int
    old_text: str
    new_text: str
    reason: str


class CodeModernizer:
    """代码现代化工具"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.replacements: List[Replacement] = []

    def modernize_file(self, filepath: str, backup: bool = False) -> bool:
        """现代化单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
        except Exception as e:
            print(f"错误：无法读取文件 {filepath}: {e}", file=sys.stderr)
            return False

        # 应用所有转换
        lines = original_lines.copy()
        self.replacements = []

        lines = self._replace_null_with_nullptr(lines)
        lines = self._replace_typedef_with_using(lines)
        lines = self._add_explicit_to_constructors(lines)
        lines = self._replace_zero_nullptr(lines)

        # 检查是否有更改
        if lines == original_lines:
            print(f"✓ {filepath}: 无需更改")
            return False

        # 显示更改
        print(f"\n📝 {filepath}:")
        for repl in self.replacements:
            print(f"  第 {repl.line_num} 行: {repl.reason}")
            print(f"    - {repl.old_text.strip()}")
            print(f"    + {repl.new_text.strip()}")

        if self.dry_run:
            print(f"  [模拟模式 - 未实际修改]")
            return True

        # 创建备份
        if backup:
            backup_path = filepath + '.bak'
            shutil.copy2(filepath, backup_path)
            print(f"  备份已创建: {backup_path}")

        # 写入修改
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"  ✓ 文件已更新")
            return True
        except Exception as e:
            print(f"  错误：无法写入文件: {e}", file=sys.stderr)
            return False

    def _replace_null_with_nullptr(self, lines: List[str]) -> List[str]:
        """替换 NULL 为 nullptr"""
        result = []
        for i, line in enumerate(lines, 1):
            new_line = line

            # 跳过注释和字符串
            if '//' not in line and '/*' not in line:
                # 替换 NULL (作为独立单词)
                if re.search(r'\bNULL\b', line):
                    old_line = line
                    new_line = re.sub(r'\bNULL\b', 'nullptr', line)
                    if old_line != new_line:
                        self.replacements.append(Replacement(
                            line_num=i,
                            old_text=old_line,
                            new_text=new_line,
                            reason="NULL → nullptr (ES.47)"
                        ))

            result.append(new_line)
        return result

    def _replace_typedef_with_using(self, lines: List[str]) -> List[str]:
        """替换 typedef 为 using"""
        result = []
        for i, line in enumerate(lines, 1):
            new_line = line

            # 匹配简单的 typedef
            match = re.match(r'(\s*)typedef\s+(.+?)\s+(\w+)\s*;', line)
            if match:
                indent, old_type, new_name = match.groups()
                old_line = line
                new_line = f"{indent}using {new_name} = {old_type};\n"

                self.replacements.append(Replacement(
                    line_num=i,
                    old_text=old_line,
                    new_text=new_line,
                    reason="typedef → using (T.43)"
                ))

            result.append(new_line)
        return result

    def _replace_zero_nullptr(self, lines: List[str]) -> List[str]:
        """替换指针赋值中的 0 为 nullptr"""
        result = []
        for i, line in enumerate(lines, 1):
            new_line = line

            # 匹配 ptr = 0;
            if re.search(r'\*\s*\w+\s*=\s*0\s*;', line):
                old_line = line
                new_line = re.sub(r'=\s*0\s*;', '= nullptr;', line)

                if old_line != new_line:
                    self.replacements.append(Replacement(
                        line_num=i,
                        old_text=old_line,
                        new_text=new_line,
                        reason="指针初始化 0 → nullptr (ES.47)"
                    ))

            result.append(new_line)
        return result

    def _add_explicit_to_constructors(self, lines: List[str]) -> List[str]:
        """为单参数构造函数添加 explicit"""
        result = []
        in_class = False
        access_level = "private"

        for i, line in enumerate(lines, 1):
            new_line = line

            # 追踪类定义
            if re.match(r'\s*(class|struct)\s+\w+', line):
                in_class = True
                access_level = "public" if "struct" in line else "private"

            # 追踪访问级别
            if re.match(r'\s*public\s*:', line):
                access_level = "public"
            elif re.match(r'\s*private\s*:', line):
                access_level = "private"
            elif re.match(r'\s*protected\s*:', line):
                access_level = "protected"

            # 检测单参数构造函数
            if in_class and access_level == "public":
                # 匹配构造函数 ClassName(Type param)
                match = re.match(r'(\s*)(\w+)\s*\(\s*\w+[^,)]*\)\s*[:{;]', line)
                if match and 'explicit' not in line and 'delete' not in line:
                    indent = match.group(1)
                    old_line = line
                    new_line = line.replace(indent, indent + 'explicit ', 1)

                    self.replacements.append(Replacement(
                        line_num=i,
                        old_text=old_line,
                        new_text=new_line,
                        reason="添加 explicit 到单参数构造函数 (C.46)"
                    ))

            # 类定义结束
            if in_class and re.match(r'\s*}\s*;', line):
                in_class = False

            result.append(new_line)
        return result


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python modernize_code.py <file.cpp> [options]")
        print("\n选项:")
        print("  --dry-run    只显示会做的更改，不实际修改文件")
        print("  --backup     修改前创建备份文件 (.bak)")
        print("\n示例:")
        print("  python modernize_code.py main.cpp --dry-run")
        print("  python modernize_code.py main.cpp --backup")
        sys.exit(1)

    filepath = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    backup = '--backup' in sys.argv

    if not os.path.isfile(filepath):
        print(f"错误: {filepath} 不是有效的文件", file=sys.stderr)
        sys.exit(1)

    modernizer = CodeModernizer(dry_run=dry_run)

    if dry_run:
        print("🔍 模拟模式 - 只显示更改，不修改文件\n")

    success = modernizer.modernize_file(filepath, backup=backup)

    if success:
        if dry_run:
            print("\n提示: 移除 --dry-run 选项以应用这些更改")
        else:
            print("\n✅ 现代化完成！")
    else:
        if not dry_run:
            print("\n已跳过 (无更改)")


if __name__ == "__main__":
    main()
