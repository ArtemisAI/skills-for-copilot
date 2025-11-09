#!/bin/bash

# 思维导图结构审查脚本
# 用途: 审查 Markdown 思维导图的结构和逻辑
# 使用: ./review-mindmap.sh <文件路径> [选项]

set -euo pipefail

# ============================================================================
# 配置和变量
# ============================================================================

VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 问题计数
ISSUE_COUNT=0
WARNING_COUNT=0

# 选项
VERBOSE=false
SUMMARY=false
JSON_OUTPUT=false

# 统计信息
stats_total_lines=0
stats_total_headings=0
stats_h1_count=0
stats_h2_count=0
stats_h3_count=0
stats_h4_count=0
stats_h5_count=0
stats_h6_count=0
stats_avg_depth=0
stats_max_depth=0
stats_leaf_nodes=0

# ============================================================================
# 辅助函数
# ============================================================================

show_help() {
    cat << EOF
思维导图结构审查工具 v${VERSION}

用途:
  审查 Markdown 思维导图的结构和逻辑,发现潜在问题

用法:
  $0 <文件路径> [选项]

选项:
  -h, --help          显示帮助信息
  -v, --verbose       详细输出模式
  -s, --summary       仅显示摘要
  -j, --json          JSON 格式输出

示例:
  $0 mindmap.md
  $0 mindmap.md -v
  $0 mindmap.md -s

EOF
}

print_color() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_issue() {
    print_color "$RED" "问题: $@"
    ISSUE_COUNT=$((ISSUE_COUNT + 1))
}

print_warning() {
    print_color "$YELLOW" "建议: $@"
    WARNING_COUNT=$((WARNING_COUNT + 1))
}

print_good() {
    print_color "$GREEN" "优点: $@"
}

verbose() {
    if [ "$VERBOSE" = true ]; then
        echo "$@"
    fi
}

# ============================================================================
# 统计函数
# ============================================================================

collect_statistics() {
    local file=$1
    verbose "收集统计信息..."

    stats_total_lines=$(wc -l < "$file")
    stats_h1_count=$(grep -c "^# " "$file" || true)
    stats_h2_count=$(grep -c "^## " "$file" || true)
    stats_h3_count=$(grep -c "^### " "$file" || true)
    stats_h4_count=$(grep -c "^#### " "$file" || true)
    stats_h5_count=$(grep -c "^##### " "$file" || true)
    stats_h6_count=$(grep -c "^###### " "$file" || true)

    stats_total_headings=$((stats_h1_count + stats_h2_count + stats_h3_count + stats_h4_count + stats_h5_count + stats_h6_count))

    # 计算最大深度
    if [ "$stats_h6_count" -gt 0 ]; then
        stats_max_depth=6
    elif [ "$stats_h5_count" -gt 0 ]; then
        stats_max_depth=5
    elif [ "$stats_h4_count" -gt 0 ]; then
        stats_max_depth=4
    elif [ "$stats_h3_count" -gt 0 ]; then
        stats_max_depth=3
    elif [ "$stats_h2_count" -gt 0 ]; then
        stats_max_depth=2
    else
        stats_max_depth=1
    fi

    # 计算平均深度
    local total_depth=$((stats_h1_count * 1 + stats_h2_count * 2 + stats_h3_count * 3 + stats_h4_count * 4 + stats_h5_count * 5 + stats_h6_count * 6))
    if [ "$stats_total_headings" -gt 0 ]; then
        stats_avg_depth=$((total_depth / stats_total_headings))
    fi

    # 计算叶子节点数（简化算法：没有子节点的标题）
    local line_num=0
    local current_level=0
    local next_level=0
    stats_leaf_nodes=0

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        if [[ "$line" =~ ^(#+)[[:space:]] ]]; then
            local hashes="${BASH_REMATCH[1]}"
            current_level=${#hashes}

            # 读取下一个标题的层级
            local next_line_num=$((line_num + 1))
            local found_next=false

            while IFS= read -r next_line; do
                if [[ "$next_line" =~ ^(#+)[[:space:]] ]]; then
                    local next_hashes="${BASH_REMATCH[1]}"
                    next_level=${#next_hashes}
                    found_next=true
                    break
                fi
            done < <(tail -n +$next_line_num "$file")

            # 如果下一个标题层级<=当前层级,说明当前节点是叶子
            if [ "$found_next" = false ] || [ "$next_level" -le "$current_level" ]; then
                stats_leaf_nodes=$((stats_leaf_nodes + 1))
            fi
        fi
    done < "$file"

    verbose "  统计信息收集完成"
}

# ============================================================================
# 结构审查函数
# ============================================================================

# 1. 内容规模审查
check_content_scale() {
    local file=$1
    verbose "审查内容规模..."

    # 节点数检查
    if [ "$stats_total_headings" -lt 10 ]; then
        print_issue "内容过少: 只有 $stats_total_headings 个节点,建议至少 10 个以上"
    elif [ "$stats_total_headings" -lt 20 ]; then
        print_warning "内容偏少: $stats_total_headings 个节点,可以考虑进一步展开"
    else
        print_good "内容充实: $stats_total_headings 个节点"
    fi

    # 深度检查
    if [ "$stats_max_depth" -lt 3 ]; then
        print_issue "层级过浅: 最大深度只有 $stats_max_depth 级,建议至少 3 级"
    elif [ "$stats_max_depth" -eq 6 ]; then
        print_warning "层级很深: 达到 6 级,考虑是否可以优化结构"
    else
        print_good "层级合理: 最大深度 $stats_max_depth 级"
    fi

    verbose "  内容规模审查完成"
}

# 2. 结构平衡性审查
check_structure_balance() {
    local file=$1
    verbose "审查结构平衡性..."

    # 叶子节点比例
    if [ "$stats_total_headings" -gt 0 ]; then
        local leaf_ratio=$((stats_leaf_nodes * 100 / stats_total_headings))

        if [ "$leaf_ratio" -lt 15 ]; then
            print_warning "叶子节点偏少: 只有 ${leaf_ratio}%,可能结构过于扁平"
        elif [ "$leaf_ratio" -gt 60 ]; then
            print_warning "叶子节点过多: 达到 ${leaf_ratio}%,可能缺少中间层级"
        else
            print_good "叶子节点比例适中: ${leaf_ratio}% ($stats_leaf_nodes/$stats_total_headings)"
        fi
    fi

    # 二级节点数量检查（主要分支）
    if [ "$stats_h2_count" -lt 3 ]; then
        print_issue "主要分支过少: 只有 $stats_h2_count 个二级标题,建议 3-7 个"
    elif [ "$stats_h2_count" -gt 7 ]; then
        print_warning "主要分支较多: $stats_h2_count 个二级标题,考虑合并相关内容"
    else
        print_good "主要分支数量合理: $stats_h2_count 个二级标题"
    fi

    verbose "  结构平衡性审查完成"
}

# 3. 单子节点检查
check_single_children() {
    local file=$1
    verbose "检查单子节点..."

    local single_child_count=0
    local prev_level=0
    local same_level_count=0
    local line_num=0
    local single_child_lines=""

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        if [[ "$line" =~ ^(#+)[[:space:]](.*)$ ]]; then
            local hashes="${BASH_REMATCH[1]}"
            local title="${BASH_REMATCH[2]}"
            local current_level=${#hashes}

            if [ "$prev_level" -gt 0 ]; then
                if [ "$current_level" -gt "$prev_level" ]; then
                    # 进入子级
                    same_level_count=1
                elif [ "$current_level" -eq "$prev_level" ]; then
                    # 同级节点
                    same_level_count=$((same_level_count + 1))
                else
                    # 返回上级,检查上一组
                    if [ "$same_level_count" -eq 1 ]; then
                        single_child_count=$((single_child_count + 1))
                        if [ -n "$single_child_lines" ]; then
                            single_child_lines="$single_child_lines, $line_num"
                        else
                            single_child_lines="$line_num"
                        fi
                    fi
                    same_level_count=1
                fi
            else
                same_level_count=1
            fi

            prev_level=$current_level
        fi
    done < "$file"

    # 计算比例
    if [ "$stats_total_headings" -gt 0 ]; then
        local single_child_ratio=$((single_child_count * 100 / stats_total_headings))

        if [ "$single_child_count" -eq 0 ]; then
            print_good "无单子节点问题"
        elif [ "$single_child_ratio" -le 10 ]; then
            print_warning "发现 $single_child_count 个单子节点 (${single_child_ratio}%),可以考虑合并或扩展"
        else
            print_issue "单子节点过多: $single_child_count 个 (${single_child_ratio}%),建议优化结构"
        fi
    fi

    verbose "  单子节点检查完成"
}

# 4. 同级节点数量检查
check_sibling_count() {
    local file=$1
    verbose "检查同级节点数量..."

    local excessive_siblings=0
    local line_num=0
    local prev_level=0
    local same_level_count=0
    local parent_line=0

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        if [[ "$line" =~ ^(#+)[[:space:]](.*)$ ]]; then
            local hashes="${BASH_REMATCH[1]}"
            local title="${BASH_REMATCH[2]}"
            local current_level=${#hashes}

            if [ "$prev_level" -gt 0 ]; then
                if [ "$current_level" -gt "$prev_level" ]; then
                    # 进入子级
                    same_level_count=1
                    parent_line=$((line_num - 1))
                elif [ "$current_level" -eq "$prev_level" ]; then
                    # 同级节点
                    same_level_count=$((same_level_count + 1))
                else
                    # 返回上级,检查上一组
                    if [ "$same_level_count" -gt 8 ]; then
                        excessive_siblings=$((excessive_siblings + 1))
                        verbose "    第 $parent_line 行下有 $same_level_count 个同级子节点"
                    fi
                    same_level_count=1
                    parent_line=$((line_num - 1))
                fi
            else
                same_level_count=1
            fi

            prev_level=$current_level
        fi
    done < "$file"

    if [ "$excessive_siblings" -eq 0 ]; then
        print_good "同级节点数量控制良好"
    else
        print_warning "发现 $excessive_siblings 处同级节点过多 (>8个),建议分组或合并"
    fi

    verbose "  同级节点数量检查完成"
}

# 5. 空白节点检查
check_empty_nodes() {
    local file=$1
    verbose "检查空白节点..."

    local empty_count=0
    local line_num=0
    local in_heading=false
    local heading_line=0
    local has_content=false

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        if [[ "$line" =~ ^#+[[:space:]] ]]; then
            # 检查上一个标题
            if $in_heading && ! $has_content && [ "$heading_line" -gt 0 ]; then
                empty_count=$((empty_count + 1))
                verbose "    第 $heading_line 行标题下无内容"
            fi

            # 开始新标题
            in_heading=true
            heading_line=$line_num
            has_content=false
        elif [ -n "$line" ] && [[ ! "$line" =~ ^[[:space:]]*$ ]]; then
            # 有非空内容
            has_content=true
        fi
    done < "$file"

    if [ "$empty_count" -eq 0 ]; then
        print_good "所有节点都有内容或子节点"
    elif [ "$stats_total_headings" -gt 0 ]; then
        local empty_ratio=$((empty_count * 100 / stats_total_headings))
        if [ "$empty_ratio" -le 10 ]; then
            print_warning "发现 $empty_count 个空白节点 (${empty_ratio}%)"
        else
            print_issue "空白节点较多: $empty_count 个 (${empty_ratio}%),建议补充内容"
        fi
    fi

    verbose "  空白节点检查完成"
}

# ============================================================================
# 报告生成
# ============================================================================

generate_report() {
    local file=$1

    if [ "$JSON_OUTPUT" = true ]; then
        generate_json_report "$file"
    else
        generate_text_report "$file"
    fi
}

generate_text_report() {
    local file=$1

    print_color "$BLUE" "================================================================================"
    print_color "$BLUE" "思维导图结构审查报告"
    print_color "$BLUE" "================================================================================"
    echo ""
    echo "文件: $file"
    echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    if [ "$SUMMARY" = false ]; then
        print_color "$CYAN" "--------------------------------------------------------------------------------"
        print_color "$CYAN" "统计信息"
        print_color "$CYAN" "--------------------------------------------------------------------------------"
        echo "总行数: $stats_total_lines"
        echo "标题数: $stats_total_headings"
        echo "最大深度: $stats_max_depth 级"
        echo "平均深度: $stats_avg_depth 级"
        echo "叶子节点: $stats_leaf_nodes"
        echo ""

        echo "层级分布:"
        [ "$stats_h1_count" -gt 0 ] && echo "  1 级: $stats_h1_count 个"
        [ "$stats_h2_count" -gt 0 ] && echo "  2 级: $stats_h2_count 个"
        [ "$stats_h3_count" -gt 0 ] && echo "  3 级: $stats_h3_count 个"
        [ "$stats_h4_count" -gt 0 ] && echo "  4 级: $stats_h4_count 个"
        [ "$stats_h5_count" -gt 0 ] && echo "  5 级: $stats_h5_count 个"
        [ "$stats_h6_count" -gt 0 ] && echo "  6 级: $stats_h6_count 个"
        echo ""
    fi

    print_color "$CYAN" "--------------------------------------------------------------------------------"
    print_color "$CYAN" "审查结果"
    print_color "$CYAN" "--------------------------------------------------------------------------------"
    echo ""

    # 执行各项审查
    check_content_scale "$file"
    echo ""
    check_structure_balance "$file"
    echo ""
    check_single_children "$file"
    echo ""
    check_sibling_count "$file"
    echo ""
    check_empty_nodes "$file"
    echo ""

    print_color "$CYAN" "--------------------------------------------------------------------------------"
    print_color "$CYAN" "总结"
    print_color "$CYAN" "--------------------------------------------------------------------------------"
    echo "问题数: $ISSUE_COUNT"
    echo "建议数: $WARNING_COUNT"
    echo ""

    if [ "$ISSUE_COUNT" -eq 0 ] && [ "$WARNING_COUNT" -eq 0 ]; then
        print_color "$GREEN" "结构良好: 未发现明显问题"
    elif [ "$ISSUE_COUNT" -eq 0 ]; then
        print_color "$GREEN" "结构合格: 有 $WARNING_COUNT 条改进建议"
    else
        print_color "$YELLOW" "发现 $ISSUE_COUNT 个问题和 $WARNING_COUNT 条建议,建议优化"
    fi

    echo ""
    print_color "$BLUE" "================================================================================"
}

generate_json_report() {
    local file=$1

    cat << EOF
{
  "file": "$file",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "statistics": {
    "total_lines": $stats_total_lines,
    "total_headings": $stats_total_headings,
    "max_depth": $stats_max_depth,
    "avg_depth": $stats_avg_depth,
    "leaf_nodes": $stats_leaf_nodes,
    "h1_count": $stats_h1_count,
    "h2_count": $stats_h2_count,
    "h3_count": $stats_h3_count,
    "h4_count": $stats_h4_count,
    "h5_count": $stats_h5_count,
    "h6_count": $stats_h6_count
  },
  "review": {
    "issues": $ISSUE_COUNT,
    "warnings": $WARNING_COUNT,
    "status": "$([ "$ISSUE_COUNT" -eq 0 ] && echo "passed" || echo "needs_improvement")"
  }
}
EOF
}

# ============================================================================
# 主函数
# ============================================================================

main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 2
    fi

    local file=""

    while [ $# -gt 0 ]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -s|--summary)
                SUMMARY=true
                shift
                ;;
            -j|--json)
                JSON_OUTPUT=true
                shift
                ;;
            -*)
                echo "未知选项: $1"
                show_help
                exit 2
                ;;
            *)
                file="$1"
                shift
                ;;
        esac
    done

    if [ -z "$file" ]; then
        echo "错误: 必须指定文件路径"
        show_help
        exit 2
    fi

    if [ ! -f "$file" ]; then
        echo "错误: 文件不存在: $file"
        exit 2
    fi

    # 收集统计信息
    collect_statistics "$file"

    # 生成报告
    generate_report "$file"

    # 根据问题数返回退出码
    if [ "$ISSUE_COUNT" -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

main "$@"
