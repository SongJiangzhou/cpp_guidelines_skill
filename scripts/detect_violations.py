#!/usr/bin/env python3
"""
C++ Core Guidelines 违规检测脚本

检测常见的 Core Guidelines 违规模式，包括：
- 裸 new/delete 使用
- NULL 而非 nullptr
- C 风格类型转换
- typedef 而非 using
- 手写循环可以用算法替代
- 缺少 const
- 等等

用法:
    python detect_violations.py <file.cpp>
    python detect_violations.py <directory> --recursive
"""

import re
import sys
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum


class Severity(Enum):
    """违规严重程度"""
    CRITICAL = "严重"  # 必须修复
    IMPORTANT = "重要"  # 应该修复
    SUGGESTION = "建议"  # 可选优化


@dataclass
class Violation:
    """违规信息"""
    file: str
    line: int
    column: int
    severity: Severity
    rule: str
    message: str
    code_snippet: str
    suggestion: str


class ViolationDetector:
    """违规检测器"""

    def __init__(self):
        self.violations: List[Violation] = []

    def detect_file(self, filepath: str) -> List[Violation]:
        """检测单个文件"""
        self.violations = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"错误：无法读取文件 {filepath}: {e}", file=sys.stderr)
            return []

        # 运行所有检测
        self._detect_raw_new_delete(filepath, lines)
        self._detect_null_usage(filepath, lines)
        self._detect_c_style_cast(filepath, lines)
        self._detect_typedef(filepath, lines)
        self._detect_missing_const(filepath, lines)
        self._detect_manual_loops(filepath, lines)
        self._detect_raw_pointers(filepath, lines)
        self._detect_c_arrays(filepath, lines)

        return self.violations

    def _detect_raw_new_delete(self, filepath: str, lines: List[str]):
        """检测裸 new/delete"""
        for i, line in enumerate(lines, 1):
            # 跳过注释
            if '//' in line:
                code_part = line.split('//')[0]
            else:
                code_part = line

            # 检测 new (但不是 placement new)
            if re.search(r'\bnew\s+\w+', code_part):
                # 排除 make_unique, make_shared
                if 'make_unique' not in line and 'make_shared' not in line:
                    self.violations.append(Violation(
                        file=filepath,
                        line=i,
                        column=line.find('new'),
                        severity=Severity.CRITICAL,
                        rule="R.11",
                        message="直接使用 'new'，应使用智能指针",
                        code_snippet=line.strip(),
                        suggestion="使用 std::make_unique<T>() 或 std::make_shared<T>()"
                    ))

            # 检测 delete
            if re.search(r'\bdelete\s+', code_part):
                self.violations.append(Violation(
                    file=filepath,
                    line=i,
                    column=line.find('delete'),
                    severity=Severity.CRITICAL,
                    rule="R.11",
                    message="直接使用 'delete'，应使用智能指针或 RAII",
                    code_snippet=line.strip(),
                    suggestion="使用 RAII 或智能指针自动管理资源"
                ))

    def _detect_null_usage(self, filepath: str, lines: List[str]):
        """检测 NULL 或 0 作为空指针"""
        for i, line in enumerate(lines, 1):
            # 跳过注释和字符串
            if '//' in line:
                code_part = line.split('//')[0]
            else:
                code_part = line

            # 检测 NULL (通常是大写)
            if re.search(r'\bNULL\b', code_part):
                self.violations.append(Violation(
                    file=filepath,
                    line=i,
                    column=line.find('NULL'),
                    severity=Severity.IMPORTANT,
                    rule="ES.47",
                    message="使用 NULL，应使用 nullptr",
                    code_snippet=line.strip(),
                    suggestion="替换为 nullptr"
                ))

            # 检测指针赋值为 0
            if re.search(r'\*\s*\w+\s*=\s*0\s*[;,)]', code_part):
                self.violations.append(Violation(
                    file=filepath,
                    line=i,
                    column=0,
                    severity=Severity.IMPORTANT,
                    rule="ES.47",
                    message="指针赋值为 0，应使用 nullptr",
                    code_snippet=line.strip(),
                    suggestion="替换为 nullptr"
                ))

    def _detect_c_style_cast(self, filepath: str, lines: List[str]):
        """检测 C 风格类型转换"""
        for i, line in enumerate(lines, 1):
            if '//' in line:
                code_part = line.split('//')[0]
            else:
                code_part = line

            # 检测 (Type)value 形式
            if re.search(r'\([A-Z]\w*\s*\*?\s*\)\s*[a-zA-Z_]', code_part):
                self.violations.append(Violation(
                    file=filepath,
                    line=i,
                    column=0,
                    severity=Severity.CRITICAL,
                    rule="ES.49",
                    message="使用 C 风格类型转换",
                    code_snippet=line.strip(),
                    suggestion="使用 static_cast<T>(), dynamic_cast<T>() 等"
                ))

    def _detect_typedef(self, filepath: str, lines: List[str]):
        """检测 typedef 而非 using"""
        for i, line in enumerate(lines, 1):
            if '//' in line:
                code_part = line.split('//')[0]
            else:
                code_part = line

            # 检测 typedef
            if re.search(r'\btypedef\b', code_part):
                self.violations.append(Violation(
                    file=filepath,
                    line=i,
                    column=line.find('typedef'),
                    severity=Severity.SUGGESTION,
                    rule="T.43",
                    message="使用 typedef，建议使用 using",
                    code_snippet=line.strip(),
                    suggestion="使用 using 别名: using NewName = OldType;"
                ))

    def _detect_missing_const(self, filepath: str, lines: List[str]):
        """检测可能缺少的 const"""
        for i, line in enumerate(lines, 1):
            # 检测成员函数可能应该是 const
            if re.search(r'^\s*(int|bool|void|string|double|float)\s+\w+\s*\([^)]*\)\s*\{', line):
                # 简单启发：如果函数体只有 return 语句
                if i < len(lines) and 'return' in lines[i] and 'const' not in line:
                    self.violations.append(Violation(
                        file=filepath,
                        line=i,
                        column=0,
                        severity=Severity.IMPORTANT,
                        rule="Con.2",
                        message="成员函数可能应该声明为 const",
                        code_snippet=line.strip(),
                        suggestion="如果函数不修改对象状态，添加 const 限定符"
                    ))

    def _detect_manual_loops(self, filepath: str, lines: List[str]):
        """检测手写循环可以用算法替代"""
        for i, line in enumerate(lines, 1):
            # 检测 for (int i = 0; i < size; ++i) 模式
            if re.search(r'for\s*\(\s*\w+\s+\w+\s*=\s*0\s*;.*\.size\(\)', line):
                self.violations.append(Violation(
                    file=filepath,
                    line=i,
                    column=0,
                    severity=Severity.SUGGESTION,
                    rule="ES.71",
                    message="使用索引循环，建议使用范围 for",
                    code_snippet=line.strip(),
                    suggestion="考虑使用 for (auto& item : container) 或标准算法"
                ))

    def _detect_raw_pointers(self, filepath: str, lines: List[str]):
        """检测函数返回裸指针"""
        for i, line in enumerate(lines, 1):
            # 检测返回指针的函数声明
            if re.search(r'\w+\s*\*\s+\w+\s*\([^)]*\)', line):
                if 'const' not in line:
                    self.violations.append(Violation(
                        file=filepath,
                        line=i,
                        column=0,
                        severity=Severity.IMPORTANT,
                        rule="I.11",
                        message="函数返回裸指针，所有权不明确",
                        code_snippet=line.strip(),
                        suggestion="考虑返回 unique_ptr、shared_ptr 或引用"
                    ))

    def _detect_c_arrays(self, filepath: str, lines: List[str]):
        """检测 C 风格数组"""
        for i, line in enumerate(lines, 1):
            # 检测数组声明 Type arr[size]
            if re.search(r'\b\w+\s+\w+\s*\[\s*\d+\s*\]', line):
                if 'char' not in line:  # 排除字符串字面量
                    self.violations.append(Violation(
                        file=filepath,
                        line=i,
                        column=0,
                        severity=Severity.SUGGESTION,
                        rule="SL.con.1",
                        message="使用 C 风格数组",
                        code_snippet=line.strip(),
                        suggestion="考虑使用 std::array<T, N> 或 std::vector<T>"
                    ))


def format_violation(v: Violation) -> str:
    """格式化违规信息为可读字符串"""
    severity_color = {
        Severity.CRITICAL: "🔴",
        Severity.IMPORTANT: "🟡",
        Severity.SUGGESTION: "🟢"
    }

    result = f"\n{severity_color[v.severity]} {v.severity.value} - {v.file}:{v.line}\n"
    result += f"   违反规则: {v.rule}\n"
    result += f"   问题: {v.message}\n"
    result += f"   代码: {v.code_snippet}\n"
    result += f"   建议: {v.suggestion}\n"

    return result


def scan_directory(directory: str, recursive: bool = False) -> List[Violation]:
    """扫描目录"""
    detector = ViolationDetector()
    all_violations = []

    pattern = "**/*.cpp" if recursive else "*.cpp"
    path = Path(directory)

    cpp_files = list(path.glob(pattern))
    cpp_files.extend(path.glob(pattern.replace('.cpp', '.h')))
    cpp_files.extend(path.glob(pattern.replace('.cpp', '.hpp')))

    for filepath in cpp_files:
        violations = detector.detect_file(str(filepath))
        all_violations.extend(violations)

    return all_violations


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python detect_violations.py <file_or_directory> [--recursive]")
        print("\n示例:")
        print("  python detect_violations.py main.cpp")
        print("  python detect_violations.py src/ --recursive")
        sys.exit(1)

    target = sys.argv[1]
    recursive = '--recursive' in sys.argv or '-r' in sys.argv

    # 检测是文件还是目录
    if os.path.isfile(target):
        detector = ViolationDetector()
        violations = detector.detect_file(target)
    elif os.path.isdir(target):
        violations = scan_directory(target, recursive)
    else:
        print(f"错误: {target} 不是有效的文件或目录", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if not violations:
        print("✅ 未检测到违规！")
        return

    # 按严重程度排序
    violations.sort(key=lambda v: (
        0 if v.severity == Severity.CRITICAL else 1 if v.severity == Severity.IMPORTANT else 2,
        v.file,
        v.line
    ))

    print(f"\n检测到 {len(violations)} 个潜在问题:\n")
    print("=" * 80)

    for v in violations:
        print(format_violation(v))

    # 统计
    critical = sum(1 for v in violations if v.severity == Severity.CRITICAL)
    important = sum(1 for v in violations if v.severity == Severity.IMPORTANT)
    suggestions = sum(1 for v in violations if v.severity == Severity.SUGGESTION)

    print("=" * 80)
    print(f"\n总计:")
    print(f"  🔴 严重问题: {critical}")
    print(f"  🟡 重要问题: {important}")
    print(f"  🟢 改进建议: {suggestions}")
    print(f"\n建议优先修复严重问题和重要问题。")


if __name__ == "__main__":
    main()
