#!/bin/bash

# 思维导图格式验证脚本
# 用途: 检查 Markdown 思维导图是否符合格式规范
# 使用: ./validate-mindmap.sh <文件路径> [选项]

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
NC='\033[0m' # No Color

# 计数器
ERROR_COUNT=0
WARNING_COUNT=0
INFO_COUNT=0

# 选项
VERBOSE=false
QUIET=false
STRICT=false
NO_COLOR=false

# 限制参数
MAX_HEADING_LEVEL=6
RECOMMENDED_MAX_LEVEL=5
MAX_SIBLINGS=7
MAX_TITLE_LENGTH=50

# ============================================================================
# 辅助函数
# ============================================================================

# 显示帮助信息
show_help() {
    cat << EOF
思维导图格式验证工具 v${VERSION}

用途:
  验证 Markdown 思维导图文件是否符合格式规范

用法:
  $0 <文件路径> [选项]

选项:
  -h, --help          显示帮助信息
  -v, --verbose       详细输出模式
  -q, --quiet         只显示错误
  -s, --strict        严格模式（警告视为错误）
  --no-color          禁用颜色输出

示例:
  $0 mindmap.md
  $0 mindmap.md -v
  $0 mindmap.md --strict

退出码:
  0 - 验证通过
  1 - 验证失败（存在错误）
  2 - 文件无法读取或处理

EOF
}

# 颜色输出
print_color() {
    local color=$1
    shift
    if [ "$NO_COLOR" = true ]; then
        echo "$@"
    else
        echo -e "${color}$@${NC}"
    fi
}

print_error() {
    print_color "$RED" "❌ ERROR: $@"
    ERROR_COUNT=$((ERROR_COUNT + 1))
}

print_warning() {
    print_color "$YELLOW" "⚠️  WARNING: $@"
    WARNING_COUNT=$((WARNING_COUNT + 1))
}

print_info() {
    if [ "$QUIET" = false ]; then
        print_color "$BLUE" "ℹ️  INFO: $@"
    fi
    INFO_COUNT=$((INFO_COUNT + 1))
}

print_success() {
    print_color "$GREEN" "✅ $@"
}

# 详细输出
verbose() {
    if [ "$VERBOSE" = true ]; then
        echo "$@"
    fi
}

# ============================================================================
# 验证函数
# ============================================================================

# 1. 文件基本检查
check_file_basics() {
    local file=$1
    verbose "检查文件基本属性..."

    # 1.1 文件存在性
    if [ ! -f "$file" ]; then
        print_error "[E001] 文件不存在或无法读取: $file"
        return 1
    fi

    # 1.2 文件编码
    local encoding=$(file -b --mime-encoding "$file")
    if [[ ! "$encoding" =~ ^(utf-8|us-ascii)$ ]]; then
        print_error "[E002] 文件编码错误 ($encoding)，必须使用 UTF-8 编码"
    fi

    # 1.3 文件扩展名
    if [[ ! "$file" =~ \.md$ ]]; then
        print_warning "[W001] 建议使用 .md 作为文件扩展名"
    fi

    # 1.4 文件非空
    if [ ! -s "$file" ]; then
        print_error "[E003] 文件为空，无有效内容"
        return 1
    fi

    verbose "  ✓ 文件基本属性检查完成"
    return 0
}

# 2. 标题层级检查
check_heading_levels() {
    local file=$1
    verbose "检查标题层级..."

    # 2.1 根节点存在性
    local first_heading=$(grep -n "^#" "$file" | head -1)
    if [ -z "$first_heading" ]; then
        print_error "[E101] 文件中没有找到任何标题"
        return 1
    fi

    local first_line=$(echo "$first_heading" | cut -d: -f1)
    local first_content=$(echo "$first_heading" | cut -d: -f2-)

    if [[ ! "$first_content" =~ ^#[^#] ]]; then
        print_error "[E101] 文件必须以一级标题 (#) 开始，当前第 $first_line 行: $first_content"
    fi

    # 2.2 根节点唯一性
    local h1_count=$(grep -c "^#[^#]" "$file" || true)
    if [ "$h1_count" -gt 1 ]; then
        print_error "[E102] 文件只能有一个一级标题，发现 $h1_count 个"
    fi

    # 2.3 标题层级连续性和最大深度
    local prev_level=0
    local line_num=0

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        # 检查是否为标题
        if [[ "$line" =~ ^(#+)[[:space:]] ]]; then
            local hashes="${BASH_REMATCH[1]}"
            local current_level=${#hashes}

            # 检查最大层级深度
            if [ "$current_level" -gt "$MAX_HEADING_LEVEL" ]; then
                print_error "[E104] 第 $line_num 行超出最大层级深度 ($MAX_HEADING_LEVEL 级)"
            elif [ "$current_level" -eq "$MAX_HEADING_LEVEL" ]; then
                print_warning "[W101] 第 $line_num 行达到 $MAX_HEADING_LEVEL 级深度，建议不超过 $RECOMMENDED_MAX_LEVEL 级"
            fi

            # 检查层级跳跃（跳级）
            if [ "$prev_level" -gt 0 ]; then
                local level_diff=$((current_level - prev_level))
                if [ "$level_diff" -gt 1 ]; then
                    local prev_symbol=$(printf '#%.0s' $(seq 1 $prev_level))
                    local curr_symbol=$(printf '#%.0s' $(seq 1 $current_level))
                    print_error "[E103] 第 $line_num 行标题层级跳级: 从 $prev_symbol 跳到 $curr_symbol"
                fi
            fi

            prev_level=$current_level
        fi
    done < "$file"

    verbose "  ✓ 标题层级检查完成"
    return 0
}

# 3. 标题格式检查
check_heading_format() {
    local file=$1
    verbose "检查标题格式..."

    local line_num=0

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        # 检查标题行
        if [[ "$line" =~ ^(#+)([^#[:space:]]) ]]; then
            # 3.1 标题格式规范（# 后必须有空格）
            print_error "[E201] 第 $line_num 行标题格式错误: # 后必须有空格"
        elif [[ "$line" =~ ^(#+)[[:space:]]+(.*)$ ]]; then
            local hashes="${BASH_REMATCH[1]}"
            local title="${BASH_REMATCH[2]}"

            # 3.2 标题非空
            if [ -z "$title" ]; then
                print_error "[E202] 第 $line_num 行标题为空"
            fi

            # 3.3 标题长度
            local title_length=${#title}
            if [ "$title_length" -gt "$MAX_TITLE_LENGTH" ]; then
                print_warning "[W201] 第 $line_num 行标题过长 ($title_length 字符)，建议不超过 $MAX_TITLE_LENGTH"
            fi
        fi
    done < "$file"

    verbose "  ✓ 标题格式检查完成"
    return 0
}

# 4. 内容结构检查
check_content_structure() {
    local file=$1
    verbose "检查内容结构..."

    # 简化版本：只检查明显的结构问题
    # 由于 macOS 默认 bash 3.x 不支持关联数组，使用简化逻辑

    local prev_level=0
    local same_level_count=0
    local line_num=0

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        if [[ "$line" =~ ^(#+)[[:space:]] ]]; then
            local hashes="${BASH_REMATCH[1]}"
            local current_level=${#hashes}

            # 4.1 单子节点检查（简化版）
            if [ "$prev_level" -gt 0 ]; then
                if [ "$current_level" -gt "$prev_level" ]; then
                    # 进入子级
                    same_level_count=1
                elif [ "$current_level" -eq "$prev_level" ]; then
                    # 同级节点
                    same_level_count=$((same_level_count + 1))
                else
                    # 返回上级，检查上一组同级节点
                    if [ "$same_level_count" -eq 1 ]; then
                        print_warning "[W301] 发现只有一个子节点的标题，建议合并或增加同级节点"
                    elif [ "$same_level_count" -gt "$MAX_SIBLINGS" ]; then
                        print_warning "[W302] 发现 $same_level_count 个同级节点，建议不超过 $MAX_SIBLINGS 个"
                    fi
                    same_level_count=1
                fi
            else
                same_level_count=1
            fi

            prev_level=$current_level
        fi
    done < "$file"

    verbose "  ✓ 内容结构检查完成"
    return 0
}

# 5. Markdown 语法检查
check_markdown_syntax() {
    local file=$1
    verbose "检查 Markdown 语法..."

    # 5.1 代码块闭合检查
    local code_block_count=$(grep -c "^\`\`\`" "$file" || true)
    if [ $((code_block_count % 2)) -ne 0 ]; then
        local first_unclosed=$(grep -n "^\`\`\`" "$file" | tail -1 | cut -d: -f1)
        print_error "[E301] 代码块未正确闭合，从第 $first_unclosed 行开始"
    fi

    # 5.2 列表格式检查（简单检查）
    local line_num=0
    while IFS= read -r line; do
        line_num=$((line_num + 1))

        # 检查可能的列表项格式问题
        if [[ "$line" =~ ^[[:space:]]*[-*+][^[:space:]] ]]; then
            print_warning "[W401] 第 $line_num 行列表格式建议: 使用 - 或 * 开头，后接空格"
        fi
    done < "$file"

    verbose "  ✓ Markdown 语法检查完成"
    return 0
}

# 6. 内容质量检查
check_content_quality() {
    local file=$1
    verbose "检查内容质量..."

    # 6.1 空白标题节点检查
    local line_num=0
    local in_heading=false
    local heading_line=0
    local has_content=false

    while IFS= read -r line; do
        line_num=$((line_num + 1))

        if [[ "$line" =~ ^#+[[:space:]] ]]; then
            # 检查上一个标题是否有内容
            if $in_heading && ! $has_content && [ "$heading_line" -gt 0 ]; then
                print_warning "[W501] 第 $heading_line 行标题下无内容且无子节点"
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

    # 6.2 重复标题检查（同级）
    # 简化版本：检查所有同样级别的标题是否重复
    local level
    for level in {1..6}; do
        local pattern=$(printf '^%s ' "$(printf '#%.0s' $(seq 1 $level))")
        local titles=$(grep "$pattern" "$file" | sed "s/$pattern//" | sort)

        # 检查重复
        local prev_title=""
        while IFS= read -r title; do
            if [ -n "$title" ] && [ "$title" = "$prev_title" ]; then
                print_info "[I501] 发现重复的 $level 级标题: $title"
            fi
            prev_title="$title"
        done <<< "$titles"
    done

    verbose "  ✓ 内容质量检查完成"
    return 0
}

# ============================================================================
# 主函数
# ============================================================================

main() {
    # 解析参数
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
            -q|--quiet)
                QUIET=true
                shift
                ;;
            -s|--strict)
                STRICT=true
                shift
                ;;
            --no-color)
                NO_COLOR=true
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

    # 开始验证
    print_color "$BLUE" "================================================================================
思维导图格式验证
================================================================================

文件: $file"

    echo ""

    # 执行各项检查
    check_file_basics "$file" || exit 2
    check_heading_levels "$file"
    check_heading_format "$file"
    check_content_structure "$file"
    check_markdown_syntax "$file"
    check_content_quality "$file"

    # 生成报告
    echo ""
    print_color "$BLUE" "--------------------------------------------------------------------------------
验证结果
--------------------------------------------------------------------------------"

    echo "总计: $ERROR_COUNT 错误, $WARNING_COUNT 警告, $INFO_COUNT 信息"
    echo ""

    # 判断结果
    local exit_code=0

    if [ "$ERROR_COUNT" -gt 0 ]; then
        print_error "验证失败: 发现 $ERROR_COUNT 个错误"
        echo ""
        echo "请修复所有错误后重新验证。"
        exit_code=1
    elif [ "$STRICT" = true ] && [ "$WARNING_COUNT" -gt 0 ]; then
        print_error "严格模式: 发现 $WARNING_COUNT 个警告（在严格模式下视为错误）"
        exit_code=1
    else
        print_success "验证通过: $file"
        if [ "$WARNING_COUNT" -gt 0 ]; then
            echo ""
            echo "建议修复 $WARNING_COUNT 个警告以提升质量。"
        fi
    fi

    echo ""
    print_color "$BLUE" "================================================================================"

    exit $exit_code
}

# 执行主函数
main "$@"
