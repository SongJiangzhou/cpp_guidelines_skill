#!/usr/bin/env python3
"""
C++ 代码审查报告生成器

生成详细的代码审查报告，包括：
- 违规统计
- 按严重程度分类
- 按规则分类
- 修复建议优先级

用法:
    python generate_report.py <directory> [--output report.md] [--format md|html|json]
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict
import argparse

# 导入违规检测器
from detect_violations import ViolationDetector, Violation, Severity, scan_directory


class ReportGenerator:
    """报告生成器"""

    def __init__(self, violations: List[Violation]):
        self.violations = violations
        self.stats = self._calculate_stats()

    def _calculate_stats(self) -> Dict:
        """计算统计信息"""
        stats = {
            'total': len(self.violations),
            'by_severity': defaultdict(int),
            'by_rule': defaultdict(int),
            'by_file': defaultdict(int),
        }

        for v in self.violations:
            stats['by_severity'][v.severity.value] += 1
            stats['by_rule'][v.rule] += 1
            stats['by_file'][v.file] += 1

        return stats

    def generate_markdown(self) -> str:
        """生成 Markdown 格式报告"""
        report = []

        # 标题
        report.append("# C++ Core Guidelines 代码审查报告\n")
        report.append(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**检测文件数:** {len(self.stats['by_file'])}\n")
        report.append(f"**发现问题数:** {self.stats['total']}\n")

        # 执行摘要
        report.append("\n## 📊 执行摘要\n")
        report.append("| 严重程度 | 数量 | 占比 |\n")
        report.append("|---------|------|------|\n")

        for severity in [Severity.CRITICAL, Severity.IMPORTANT, Severity.SUGGESTION]:
            count = self.stats['by_severity'].get(severity.value, 0)
            percentage = (count / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
            emoji = "🔴" if severity == Severity.CRITICAL else "🟡" if severity == Severity.IMPORTANT else "🟢"
            report.append(f"| {emoji} {severity.value} | {count} | {percentage:.1f}% |\n")

        # 按规则统计
        report.append("\n## 📋 按规则统计\n")
        report.append("| 规则 | 数量 | 说明 |\n")
        report.append("|------|------|------|\n")

        rule_descriptions = {
            'R.11': '避免直接使用 new/delete',
            'ES.47': '使用 nullptr 而非 NULL',
            'ES.49': '避免 C 风格类型转换',
            'T.43': '使用 using 而非 typedef',
            'Con.2': '成员函数应该是 const',
            'ES.71': '优先使用范围 for',
            'I.11': '明确所有权语义',
            'SL.con.1': '使用标准库容器'
        }

        for rule, count in sorted(self.stats['by_rule'].items(), key=lambda x: -x[1]):
            desc = rule_descriptions.get(rule, '参见 Core Guidelines')
            report.append(f"| {rule} | {count} | {desc} |\n")

        # 按文件统计
        report.append("\n## 📁 按文件统计\n")
        report.append("| 文件 | 问题数 |\n")
        report.append("|------|--------|\n")

        for file, count in sorted(self.stats['by_file'].items(), key=lambda x: -x[1])[:10]:
            report.append(f"| {os.path.basename(file)} | {count} |\n")

        # 严重问题详情
        critical = [v for v in self.violations if v.severity == Severity.CRITICAL]
        if critical:
            report.append("\n## 🔴 严重问题详情（必须修复）\n")
            for i, v in enumerate(critical, 1):
                report.append(f"\n### {i}. {v.file}:{v.line}\n")
                report.append(f"**规则:** {v.rule} | **问题:** {v.message}\n\n")
                report.append("```cpp\n")
                report.append(f"{v.code_snippet}\n")
                report.append("```\n\n")
                report.append(f"**修复建议:** {v.suggestion}\n")

        # 重要问题详情
        important = [v for v in self.violations if v.severity == Severity.IMPORTANT]
        if important:
            report.append("\n## 🟡 重要问题详情（应该修复）\n")
            for i, v in enumerate(important[:10], 1):  # 只显示前10个
                report.append(f"\n### {i}. {v.file}:{v.line}\n")
                report.append(f"**规则:** {v.rule} | **问题:** {v.message}\n\n")
                report.append("```cpp\n")
                report.append(f"{v.code_snippet}\n")
                report.append("```\n\n")
                report.append(f"**修复建议:** {v.suggestion}\n")

            if len(important) > 10:
                report.append(f"\n*还有 {len(important) - 10} 个重要问题未显示...*\n")

        # 建议
        report.append("\n## 💡 修复建议\n")
        report.append("\n### 优先级排序\n\n")
        report.append("1. **立即修复（严重）：** 影响内存安全、类型安全的问题\n")
        report.append("2. **尽快修复（重要）：** 影响代码质量和可维护性的问题\n")
        report.append("3. **计划修复（建议）：** 代码现代化和优化建议\n")

        report.append("\n### 推荐工具\n\n")
        report.append("- **clang-tidy:** 自动检测大部分 Core Guidelines 违规\n")
        report.append("- **modernize_code.py:** 自动化现代化转换\n")
        report.append("- **cppcheck:** 检测内存泄漏和错误\n")

        return ''.join(report)

    def generate_html(self) -> str:
        """生成 HTML 格式报告"""
        html = []
        html.append("<!DOCTYPE html>\n")
        html.append("<html>\n<head>\n")
        html.append("<meta charset='utf-8'>\n")
        html.append("<title>C++ Core Guidelines 审查报告</title>\n")
        html.append("<style>\n")
        html.append("body { font-family: Arial, sans-serif; margin: 40px; }\n")
        html.append("h1 { color: #333; }\n")
        html.append("table { border-collapse: collapse; width: 100%; margin: 20px 0; }\n")
        html.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n")
        html.append("th { background-color: #4CAF50; color: white; }\n")
        html.append(".critical { color: #d32f2f; }\n")
        html.append(".important { color: #f57c00; }\n")
        html.append(".suggestion { color: #388e3c; }\n")
        html.append("pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }\n")
        html.append("</style>\n</head>\n<body>\n")

        html.append("<h1>C++ Core Guidelines 代码审查报告</h1>\n")
        html.append(f"<p><strong>生成时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n")
        html.append(f"<p><strong>总问题数:</strong> {self.stats['total']}</p>\n")

        # 统计表格
        html.append("<h2>统计概览</h2>\n")
        html.append("<table>\n")
        html.append("<tr><th>严重程度</th><th>数量</th><th>占比</th></tr>\n")

        for severity in [Severity.CRITICAL, Severity.IMPORTANT, Severity.SUGGESTION]:
            count = self.stats['by_severity'].get(severity.value, 0)
            percentage = (count / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
            css_class = severity.value.lower()
            html.append(f"<tr class='{css_class}'><td>{severity.value}</td><td>{count}</td><td>{percentage:.1f}%</td></tr>\n")

        html.append("</table>\n")

        # 问题列表
        html.append("<h2>问题详情</h2>\n")
        for v in self.violations[:50]:  # 限制显示数量
            css_class = v.severity.value.lower()
            html.append(f"<div class='{css_class}' style='margin: 20px 0; padding: 10px; border-left: 4px solid;'>\n")
            html.append(f"<h3>{v.file}:{v.line}</h3>\n")
            html.append(f"<p><strong>规则:</strong> {v.rule} | <strong>问题:</strong> {v.message}</p>\n")
            html.append(f"<pre>{v.code_snippet}</pre>\n")
            html.append(f"<p><strong>建议:</strong> {v.suggestion}</p>\n")
            html.append("</div>\n")

        html.append("</body>\n</html>\n")
        return ''.join(html)

    def generate_json(self) -> str:
        """生成 JSON 格式报告"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': self.stats['total'],
                'by_severity': dict(self.stats['by_severity']),
                'by_rule': dict(self.stats['by_rule']),
                'by_file': dict(self.stats['by_file'])
            },
            'violations': [
                {
                    'file': v.file,
                    'line': v.line,
                    'column': v.column,
                    'severity': v.severity.value,
                    'rule': v.rule,
                    'message': v.message,
                    'code': v.code_snippet,
                    'suggestion': v.suggestion
                }
                for v in self.violations
            ]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成 C++ Core Guidelines 代码审查报告')
    parser.add_argument('directory', help='要分析的目录')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['md', 'html', 'json'], default='md',
                        help='输出格式 (默认: md)')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='递归扫描子目录')

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"错误: {args.directory} 不是有效的目录", file=sys.stderr)
        sys.exit(1)

    print(f"正在扫描 {args.directory}...")
    violations = scan_directory(args.directory, args.recursive)

    if not violations:
        print("✅ 未检测到违规！")
        return

    print(f"检测到 {len(violations)} 个问题，正在生成报告...")

    generator = ReportGenerator(violations)

    # 生成报告
    if args.format == 'md':
        report = generator.generate_markdown()
    elif args.format == 'html':
        report = generator.generate_html()
    else:  # json
        report = generator.generate_json()

    # 输出报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已生成: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
