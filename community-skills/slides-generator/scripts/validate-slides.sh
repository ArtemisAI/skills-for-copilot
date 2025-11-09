#!/bin/bash

# Slidev 幻灯片验证脚本
# 用途: 检查生成的幻灯片是否符合规范
# 使用: ./scripts/validate-slides.sh <slides-file.md> [--verbose] [--json]

# 注意: 不使用 set -e, 因为某些检查命令(如 grep)在没有匹配时会返回非零状态

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 选项
VERBOSE=false
JSON_OUTPUT=false

# 检查项计数
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# 输出函数
print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📋 Slidev 幻灯片规范验证${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_result() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📊 验证结果${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "总检查项: ${TOTAL_CHECKS}"
    echo -e "${GREEN}✓ 通过: ${PASSED_CHECKS}${NC}"
    echo -e "${RED}✗ 失败: ${FAILED_CHECKS}${NC}"
    echo -e "${YELLOW}⚠ 警告: ${WARNING_CHECKS}${NC}"

    if [ $FAILED_CHECKS -eq 0 ]; then
        echo -e "\n${GREEN}🎉 验证通过！幻灯片符合规范。${NC}\n"
        exit 0
    else
        echo -e "\n${RED}❌ 验证失败！请修复上述问题。${NC}\n"
        exit 1
    fi
}

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    echo -e "  ${RED}→${NC} $2"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    echo -e "  ${YELLOW}→${NC} $2"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --help|-h)
            echo "Slidev 幻灯片验证脚本"
            echo ""
            echo "用法: $0 <slides-file.md> [选项]"
            echo ""
            echo "选项:"
            echo "  --verbose, -v    显示详细信息 (包括行号)"
            echo "  --json           以 JSON 格式输出结果"
            echo "  --help, -h       显示此帮助信息"
            echo ""
            echo "示例:"
            echo "  $0 slides.md"
            echo "  $0 slides.md --verbose"
            echo "  $0 slides.md --json"
            exit 0
            ;;
        *)
            FILE="$1"
            shift
            ;;
    esac
done

# 检查文件参数
if [ -z "$FILE" ]; then
    echo -e "${RED}错误: 请提供幻灯片文件路径${NC}"
    echo "使用方法: $0 <slides-file.md>"
    echo "运行 $0 --help 查看更多选项"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo -e "${RED}错误: 文件不存在: $FILE${NC}"
    exit 1
fi

print_header
echo -e "验证文件: ${BLUE}$FILE${NC}"

# 文件信息
FILE_SIZE=$(du -h "$FILE" | cut -f1)
FILE_LINES=$(wc -l < "$FILE")
echo -e "文件大小: ${CYAN}$FILE_SIZE${NC}  |  行数: ${CYAN}$FILE_LINES${NC}\n"

# ============================================
# 1. 文件格式检查
# ============================================
echo -e "${BLUE}[1/7]${NC} 文件格式检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查 UTF-8 编码
if file "$FILE" | grep -q "UTF-8"; then
    check_pass "文件使用 UTF-8 编码"
else
    check_fail "文件编码错误" "必须使用 UTF-8 编码"
fi

# 检查换行符
if file "$FILE" | grep -q "CRLF" 2>/dev/null; then
    check_warn "文件使用 CRLF 换行符" "推荐使用 LF 换行符"
elif file "$FILE" | grep -q "text" 2>/dev/null; then
    check_pass "文件使用正确的换行符"
else
    check_pass "文件换行符检查通过"
fi

# ============================================
# 2. Frontmatter 检查
# ============================================
echo -e "\n${BLUE}[2/7]${NC} Frontmatter 配置检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查是否有 headmatter
if head -n 1 "$FILE" | grep -q "^---$"; then
    check_pass "存在 headmatter"

    # 提取 headmatter
    HEADMATTER=$(awk '/^---$/{flag=!flag; if(!flag) exit} flag' "$FILE")

    # 检查必需字段: theme
    if echo "$HEADMATTER" | grep -q "^theme:"; then
        THEME=$(echo "$HEADMATTER" | grep "^theme:" | awk '{print $2}')
        check_pass "包含 theme 配置: $THEME"
    else
        check_fail "缺少 theme 配置" "必须指定主题"
    fi

    # 检查必需字段: title
    if echo "$HEADMATTER" | grep -q "^title:"; then
        check_pass "包含 title 配置"
    else
        check_fail "缺少 title 配置" "必须指定标题"
    fi

    # 检查推荐字段: fonts
    if echo "$HEADMATTER" | grep -q "^fonts:"; then
        check_pass "包含字体配置"
    else
        check_warn "缺少字体配置" "推荐配置中文字体"
    fi

else
    check_fail "缺少 headmatter" "文件必须以 --- 开头"
fi

# ============================================
# 3. 分页规则检查
# ============================================
echo -e "\n${BLUE}[3/7]${NC} 分页规则检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 统计分隔符数量
SEPARATOR_COUNT=$(grep -c "^---$" "$FILE" || true)
SLIDE_COUNT=$((SEPARATOR_COUNT / 2))

if [ $SLIDE_COUNT -gt 0 ]; then
    check_pass "幻灯片数量: $SLIDE_COUNT 张"
else
    check_fail "没有发现幻灯片分隔符" "使用 --- 分隔幻灯片"
fi

# 检查分隔符前后是否有空行
INVALID_SEPARATORS=$(grep -n "^---$" "$FILE" | while read line; do
    LINE_NUM=$(echo "$line" | cut -d: -f1)
    PREV_LINE=$((LINE_NUM - 1))
    NEXT_LINE=$((LINE_NUM + 1))

    if [ $PREV_LINE -gt 1 ]; then
        PREV_CONTENT=$(sed -n "${PREV_LINE}p" "$FILE")
        NEXT_CONTENT=$(sed -n "${NEXT_LINE}p" "$FILE")

        if [ ! -z "$PREV_CONTENT" ] && [ ! -z "$NEXT_CONTENT" ]; then
            echo "$LINE_NUM"
        fi
    fi
done | wc -l)

if [ "$INVALID_SEPARATORS" -eq 0 ]; then
    check_pass "分隔符前后有空行"
else
    check_warn "发现 $INVALID_SEPARATORS 处分隔符前后缺少空行" "--- 前后应有空行"
fi

# ============================================
# 4. 代码块检查
# ============================================
echo -e "\n${BLUE}[4/7]${NC} 代码块规范检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查代码块是否有语言标识
# 统计有语言标识的代码块开始标记
WITH_LANG=$(grep -c '^```[a-z]' "$FILE" || true)
# 统计所有代码块标记(开始+结束)
ALL_MARKS=$(grep -c '^```' "$FILE" || true)
# 总代码块数 = 所有标记 / 2
TOTAL_CODE_BLOCKS=$((ALL_MARKS / 2))
# 无语言标识的代码块 = 总数 - 有语言标识的
WITHOUT_LANG=$((TOTAL_CODE_BLOCKS - WITH_LANG))

if [ $WITHOUT_LANG -eq 0 ]; then
    check_pass "所有代码块都有语言标识"
else
    check_fail "发现 $WITHOUT_LANG 个无语言标识的代码块" "代码块必须指定语言: \`\`\`typescript 或 \`\`\`text"

    # 详细模式: 显示无语言标识代码块的位置
    if [ "$VERBOSE" = true ]; then
        echo -e "  ${CYAN}→${NC} 无语言标识的代码块位置:"
        # 找到所有 ``` 标记，判断哪些是无语言标识的开始标记
        awk '
            /^```[a-z]/ { in_code=1; next }
            /^```$/ {
                if (in_code) {
                    in_code=0
                } else {
                    print "    行 " NR ": 缺少语言标识"
                    in_code=1
                }
            }
        ' "$FILE" | head -5

        if [ $WITHOUT_LANG -gt 5 ]; then
            echo -e "    ${CYAN}... 还有 $((WITHOUT_LANG - 5)) 处${NC}"
        fi
    fi
fi

if [ $TOTAL_CODE_BLOCKS -gt 0 ]; then
    echo -e "  ${BLUE}→${NC} 代码块总数: $TOTAL_CODE_BLOCKS (有语言: $WITH_LANG, 无语言: $WITHOUT_LANG)"
fi

# ============================================
# 5. Mermaid 图表检查
# ============================================
echo -e "\n${BLUE}[5/7]${NC} Mermaid 图表检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

MERMAID_COUNT=$(grep -c '^```mermaid' "$FILE" || true)

if [ $MERMAID_COUNT -gt 0 ]; then
    check_pass "包含 $MERMAID_COUNT 个 Mermaid 图表"

    # 检查是否有 scale 参数
    MERMAID_WITH_SCALE=$(grep -c '^```mermaid.*{scale:' "$FILE" || true)

    if [ $MERMAID_WITH_SCALE -eq $MERMAID_COUNT ]; then
        check_pass "所有 Mermaid 图表都设置了 scale 参数"
    else
        MISSING_SCALE=$((MERMAID_COUNT - MERMAID_WITH_SCALE))
        check_warn "$MISSING_SCALE 个 Mermaid 图表缺少 scale 参数" "推荐使用 {scale: 0.75}"
    fi
else
    echo -e "  ${BLUE}→${NC} 未使用 Mermaid 图表"
fi

# ============================================
# 6. 内容溢出检查
# ============================================
echo -e "\n${BLUE}[6/7]${NC} 内容溢出防止检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查是否使用了滚动或缩放
PAGES_WITH_SCROLL=$(grep -c '^class: overflow-y-auto' "$FILE" || true)
PAGES_WITH_ZOOM=$(grep -c '^zoom: ' "$FILE" || true)

if [ $PAGES_WITH_SCROLL -gt 0 ]; then
    check_pass "$PAGES_WITH_SCROLL 个页面启用了滚动"
fi

if [ $PAGES_WITH_ZOOM -gt 0 ]; then
    check_pass "$PAGES_WITH_ZOOM 个页面使用了缩放"
fi

# 检查可能需要溢出处理的页面
# 简单启发式: Mermaid + 多行文本
POTENTIAL_OVERFLOW=$(awk '
    /^---$/ { in_slide = !in_slide; lines = 0; has_mermaid = 0; next }
    in_slide && /^```mermaid/ { has_mermaid = 1 }
    in_slide && /^[^`]/ { lines++ }
    /^---$/ && has_mermaid && lines > 10 { print "potential" }
' "$FILE" | wc -l)

if [ "$POTENTIAL_OVERFLOW" -gt 0 ]; then
    HANDLED=$((PAGES_WITH_SCROLL + PAGES_WITH_ZOOM))
    if [ $HANDLED -ge $POTENTIAL_OVERFLOW ]; then
        check_pass "内容较多的页面已处理溢出问题"
    else
        UNHANDLED=$((POTENTIAL_OVERFLOW - HANDLED))
        check_warn "$UNHANDLED 个页面可能需要溢出处理" "考虑添加 class: overflow-y-auto 或 zoom"
    fi
fi

# ============================================
# 7. 内容质量检查
# ============================================
echo -e "\n${BLUE}[7/7]${NC} 内容质量检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查是否有空幻灯片
EMPTY_SLIDES=$(awk '
    BEGIN { slide_content = "" }
    /^---$/ {
        if (slide_content ~ /^[[:space:]]*$/ && NR > 10) print NR
        slide_content = ""
        next
    }
    { slide_content = slide_content $0 }
' "$FILE" | wc -l)

if [ "$EMPTY_SLIDES" -eq 0 ]; then
    check_pass "没有空白幻灯片"
else
    check_warn "发现 $EMPTY_SLIDES 个空白幻灯片" "检查是否为多余的分隔符"
fi

# 检查标题层级
SLIDE_TITLES=$(grep -c '^## ' "$FILE" || true)

if [ $SLIDE_TITLES -gt 0 ]; then
    check_pass "使用了 $SLIDE_TITLES 个幻灯片标题"
else
    check_warn "没有使用 ## 标题" "推荐每张幻灯片使用 ## 标题"
fi

# ============================================
# 输出结果
# ============================================
print_result
