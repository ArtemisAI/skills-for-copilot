# Step 1: 代码变更提取

## 目标

从 Git 提交历史中提取变更信息,识别修改的文件、类和方法。

## 输入

用户提供的 Git 范围:

- "近N次提交" → `HEAD~N..HEAD`
- "feature/xxx 分支" → `main..feature/xxx`
- "commit hash" → `hash1..hash2`
- "本分支所有提交" → `main..HEAD`

## 执行流程

### 1. 解析 Git 范围

```bash
# 近N次提交
git log -n 3 --oneline

# 特定分支对比
git log main..feature/login --oneline

# 获取提交数量
git rev-list --count HEAD~3..HEAD
```

### 2. 提取变更文件列表

```bash
# 获取变更文件
git diff --name-status HEAD~3..HEAD

# 输出示例:
# M    src/main/java/com/example/UserController.java
# A    src/main/java/com/example/SmsService.java
# D    src/main/java/com/example/OldService.java
```

**文件分类**:

- `M` (Modified): 修改的文件
- `A` (Added): 新增的文件
- `D` (Deleted): 删除的文件
- `R` (Renamed): 重命名的文件

### 3. 提取具体变更内容

```bash
# 获取详细 diff
git diff HEAD~3..HEAD

# 获取每个文件的变更统计
git diff --stat HEAD~3..HEAD
```

### 4. 识别变更的类和方法

**Java 示例**:

```bash
# 提取变更的方法签名
git diff -U0 HEAD~3..HEAD -- "*.java" | grep -E "^\+.*public|private|protected"
```

**识别重点**:

- 新增/修改的类
- 新增/修改的方法
- 修改的注解 (`@Transactional`, `@RestController` 等)
- 修改的依赖注入 (`@Autowired`, `@Inject`)

### 5. 评估变更规模

统计变更数据:

- 变更文件数量
- 新增代码行数 (`+`)
- 删除代码行数 (`-`)
- 净变更行数
- 涉及的包/模块

```bash
git diff --shortstat HEAD~3..HEAD
# 输出: 8 files changed, 245 insertions(+), 67 deletions(-)
```

## 输出

生成变更摘要:

```json
{
  "git_range": "HEAD~3..HEAD",
  "commit_count": 3,
  "commits": [
    {
      "hash": "abc1234",
      "message": "feat: 添加手机号登录功能",
      "author": "张三",
      "date": "2025-10-26 10:30"
    }
  ],
  "changed_files": [
    {
      "path": "src/main/java/com/example/UserController.java",
      "status": "M",
      "additions": 45,
      "deletions": 12,
      "changed_methods": [
        "login()",
        "sendSmsCode()"
      ]
    }
  ],
  "stats": {
    "total_files": 8,
    "total_additions": 245,
    "total_deletions": 67
  }
}
```

## MCP 工具使用

**不使用 MCP**: 此步骤仅使用 Git 命令即可完成。

## 注意事项

1. **大规模变更**: 如果变更文件 >20 个,建议分批分析
2. **二进制文件**: 忽略图片、jar 包等二进制文件
3. **生成代码**: 忽略自动生成的代码 (target/, build/, node_modules/)
4. **本地检查**: 在提测前本地执行,不依赖 CI/CD

## 常见问题

**Q: 如何排除自动生成的代码?**

A: 使用 `.gitattributes` 或在分析时过滤:

```bash
git diff HEAD~3..HEAD -- ':!target' ':!build' ':!*.min.js'
```

**Q: 如何处理 merge commit?**

A: 使用 `--first-parent` 只看主线提交:

```bash
git log --first-parent main..feature/login
```

## 下一步

→ **Step 2**: 技术栈识别 (@step2-techstack-detect.md)
