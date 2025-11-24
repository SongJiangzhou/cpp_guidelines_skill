#!/usr/bin/env python3
"""
Clang-Tidy 包装器脚本

运行 clang-tidy 并格式化输出，专注于 C++ Core Guidelines 检查

用法:
    python run_clang_tidy.py <file_or_directory> [--fix]

选项:
    --fix       自动应用修复建议（谨慎使用）
    --checks    指定检查规则（默认：cppcoreguidelines-*）
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from typing import List, Dict
import argparse


class ClangTidyRunner:
    """Clang-Tidy 运行器"""

    # C++ Core Guidelines 相关检查
    CORE_GUIDELINES_CHECKS = [
        'cppcoreguidelines-*',
        'modernize-*',
        'readability-*',
        'performance-*',
    ]

    def __init__(self, fix: bool = False, extra_checks: List[str] = None):
        self.fix = fix
        self.checks = self.CORE_GUIDELINES_CHECKS.copy()
        if extra_checks:
            self.checks.extend(extra_checks)

    def check_clang_tidy_installed(self) -> bool:
        """检查 clang-tidy 是否已安装"""
        try:
            result = subprocess.run(
                ['clang-tidy', '--version'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def run_on_file(self, filepath: str) -> Dict:
        """在单个文件上运行 clang-tidy"""
        checks_str = ','.join(self.checks)

        cmd = [
            'clang-tidy',
            f'--checks={checks_str}',
            filepath,
            '--'  # 编译选项分隔符
        ]

        if self.fix:
            cmd.insert(1, '--fix')

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            return {
                'file': filepath,
                'success': True,
                'output': result.stdout,
                'errors': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                'file': filepath,
                'success': False,
                'output': '',
                'errors': '超时（>60秒）'
            }
        except Exception as e:
            return {
                'file': filepath,
                'success': False,
                'output': '',
                'errors': str(e)
            }

    def parse_output(self, output: str) -> List[Dict]:
        """解析 clang-tidy 输出"""
        warnings = []
        lines = output.split('\n')

        for line in lines:
            # 匹配警告行格式: file:line:col: warning: message [check-name]
            if ': warning:' in line or ': error:' in line:
                parts = line.split(':', 4)
                if len(parts) >= 5:
                    try:
                        file = parts[0]
                        line_num = int(parts[1])
                        col = int(parts[2])
                        severity = parts[3].strip()
                        message = parts[4].strip()

                        # 提取检查规则名称
                        check_name = ''
                        if '[' in message and ']' in message:
                            check_name = message[message.rfind('[')+1:message.rfind(']')]
                            message = message[:message.rfind('[')].strip()

                        warnings.append({
                            'file': file,
                            'line': line_num,
                            'column': col,
                            'severity': severity,
                            'message': message,
                            'check': check_name
                        })
                    except (ValueError, IndexError):
                        continue

        return warnings

    def format_warnings(self, warnings: List[Dict]) -> str:
        """格式化警告输出"""
        if not warnings:
            return "✅ 未发现问题！\n"

        # 按规则分组
        by_check = {}
        for w in warnings:
            check = w['check'] or '其他'
            if check not in by_check:
                by_check[check] = []
            by_check[check].append(w)

        output = []
        output.append(f"\n发现 {len(warnings)} 个问题:\n")
        output.append("=" * 80 + "\n")

        # 按检查规则输出
        for check, items in sorted(by_check.items()):
            output.append(f"\n### {check} ({len(items)} 个)\n")

            # 显示前几个示例
            for w in items[:3]:
                output.append(f"\n📍 {w['file']}:{w['line']}:{w['column']}\n")
                output.append(f"   {w['message']}\n")

            if len(items) > 3:
                output.append(f"   ... 还有 {len(items) - 3} 个类似问题\n")

        return ''.join(output)


def find_cpp_files(path: str, recursive: bool = True) -> List[str]:
    """查找 C++ 文件"""
    path_obj = Path(path)

    if path_obj.is_file():
        return [str(path_obj)]

    cpp_files = []
    pattern = '**/*' if recursive else '*'

    for ext in ['.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp', '.hh', '.hxx']:
        cpp_files.extend([str(p) for p in path_obj.glob(f'{pattern}{ext}')])

    return cpp_files


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='运行 Clang-Tidy 进行 C++ Core Guidelines 检查'
    )
    parser.add_argument('path', help='文件或目录路径')
    parser.add_argument('--fix', action='store_true',
                        help='自动应用修复（谨慎使用）')
    parser.add_argument('--checks', help='额外的检查规则（逗号分隔）')
    parser.add_argument('--no-recursive', action='store_true',
                        help='不递归扫描子目录')

    args = parser.parse_args()

    runner = ClangTidyRunner(
        fix=args.fix,
        extra_checks=args.checks.split(',') if args.checks else None
    )

    # 检查 clang-tidy 是否安装
    if not runner.check_clang_tidy_installed():
        print("错误: 未找到 clang-tidy", file=sys.stderr)
        print("\n安装方法:", file=sys.stderr)
        print("  Ubuntu/Debian: sudo apt install clang-tidy", file=sys.stderr)
        print("  macOS: brew install llvm", file=sys.stderr)
        print("  其他: 请参考 https://clang.llvm.org/extra/clang-tidy/", file=sys.stderr)
        sys.exit(1)

    # 查找文件
    cpp_files = find_cpp_files(args.path, not args.no_recursive)

    if not cpp_files:
        print(f"错误: 在 {args.path} 中未找到 C++ 文件", file=sys.stderr)
        sys.exit(1)

    print(f"找到 {len(cpp_files)} 个 C++ 文件")
    if args.fix:
        print("⚠️  警告: 将自动应用修复！")

    print(f"\n正在运行 clang-tidy...")
    print(f"检查规则: {', '.join(runner.checks)}\n")

    all_warnings = []

    for i, filepath in enumerate(cpp_files, 1):
        print(f"[{i}/{len(cpp_files)}] 检查 {os.path.basename(filepath)}...", end='')

        result = runner.run_on_file(filepath)

        if result['success']:
            warnings = runner.parse_output(result['output'])
            all_warnings.extend(warnings)

            if warnings:
                print(f" {len(warnings)} 个问题")
            else:
                print(" ✓")
        else:
            print(f" ✗ 失败")
            print(f"   错误: {result['errors']}")

    # 输出汇总
    print("\n" + "=" * 80)
    print(runner.format_warnings(all_warnings))

    # 统计
    if all_warnings:
        print("\n统计信息:")
        check_counts = {}
        for w in all_warnings:
            check = w['check'] or '其他'
            check_counts[check] = check_counts.get(check, 0) + 1

        for check, count in sorted(check_counts.items(), key=lambda x: -x[1]):
            print(f"  {check}: {count}")

        print(f"\n总计: {len(all_warnings)} 个问题")

        if args.fix:
            print("\n✅ 已应用自动修复")
        else:
            print("\n提示: 使用 --fix 选项自动修复部分问题")


if __name__ == "__main__":
    main()
