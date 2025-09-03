# Lesson 2: 自定义 Slash 命令

## 🎯 学习目标

- 理解自定义 Slash 命令的概念和优势
- 创建可复用的命令模板
- 掌握命令链式工作流的构建
- 实际应用：调试分析、性能审计、安全扫描

## 📖 理论基础

### 什么是自定义 Slash 命令？

自定义 Slash 命令是存储在 `.claude/commands/` 目录中的 Markdown 模板文件，用于：

- **标准化工作流** - 每次都按相同的专业流程分析
- **专家级输出** - 结构化、专业的分析报告
- **团队共享** - 可以 commit 到 git，整个团队使用
- **可复用性** - 一次创建，反复使用

### 命令的工作原理

1. **创建模板** - 在 `.claude/commands/` 创建 `.md` 文件
2. **内容作为 Prompt** - 文件内容作为系统提示
3. **Slash 调用** - 使用 `/命令名 文件参数` 调用
4. **自动执行** - Claude 根据模板执行相应任务

## 🚀 实战演练

### 步骤 1: 创建第一个自定义命令

```bash
# 创建调试分析命令
mkdir -p .claude/commands
```

创建 `.claude/commands/debug-loop.md`:
```markdown
# Debug Loop 分析

你是一个资深的调试专家。请按照以下步骤分析错误日志：

## 分析流程
1. **识别根本原因**
2. **提供修复方案**
3. **预防未来类似问题**

请分析以下错误日志：
```

### 步骤 2: 创建测试数据

创建 `error-log.txt`:
```
2025-01-15 14:23:45 [ERROR] Database connection failed
2025-01-15 14:23:45 [ERROR] Connection timeout after 5000ms
2025-01-15 14:23:46 [WARN] Retrying connection (attempt 1/3)
```

### 步骤 3: 使用命令

```bash
/debug-loop @error-log.txt
```

## 📚 实用命令模板

### 1. 性能审计命令

`.claude/commands/performance-audit.md`:
```markdown
# 性能审计分析

你是一个性能优化专家。请分析性能问题：

## 审计维度
1. **热点识别** - 找出真正的性能瓶颈
2. **数据结构审查** - 坏程序员担心代码，好程序员担心数据结构
3. **算法复杂度** - 识别 O(n²) 的垃圾算法
4. **内存使用** - 找出内存泄漏和不必要的分配
5. **I/O 优化** - 数据库查询和网络请求分析

请分析目标代码/系统：
```

### 2. 安全审查命令

`.claude/commands/security-review.md`:
```markdown
# 安全审查

你是一个资深的安全专家。请对代码进行全面的安全审查：

## 审查清单
1. **输入验证** - 所有外部输入是否验证？
2. **SQL 注入** - 数据库查询是否使用参数化查询？
3. **XSS 防护** - 输出是否正确转义？
4. **权限控制** - 敏感操作是否有权限检查？
5. **敏感数据** - 密钥、密码是否硬编码？

请审查以下代码：
```

### 3. Linus 风格审查

`.claude/commands/linus-review.md`:
```markdown
# Linus 风格代码审查

你是 Linus Torvalds。请用你的"好品味"哲学审查这段代码：

## 审查维度
1. **品味评分** - 🟢 好品味 / 🟡 凑合 / 🔴 垃圾
2. **特殊情况分析** - 找出所有不必要的 if/else 分支
3. **数据结构审查** - "坏程序员担心代码，好程序员担心数据结构"
4. **3层缩进规则** - 超过3层的都是设计问题

请审查以下代码：
```

## 🔄 高级技巧：链式命令

### 创建多 Agent 工作流命令

`.claude/commands/marketing-analysis.md`:
```markdown
# 营销数据链式分析

执行完整的营销数据分析工作流：

## 阶段1: 数据分析
使用 marketing-data-analyzer agent：
- 计算关键指标 (CTR、转化率、ROI)
- 识别表现最差的广告
- 提供数据洞察

## 阶段2: 优化建议  
使用 ad-optimizer agent：
- 为失败广告生成优化方案
- 提供新的广告变体建议
- 制定投放策略

请分析以下营销数据文件：
```

### 代码质量流水线

`.claude/commands/code-pipeline.md`:
```markdown
# 代码质量流水线

执行完整的代码质量检查流水线：

### 1. Linus 代码审查
使用 linus-code-reviewer agent

### 2. 安全漏洞扫描
自动进行安全审查

### 3. 重构计划制定
基于前面的分析结果制定重构计划

请分析以下代码文件：
```

## 💡 最佳实践

### 1. 命令命名规范
```bash
✅ 好的命名：
- debug-loop
- performance-audit
- security-review
- marketing-analysis

❌ 避免的命名：
- command1
- analyze
- help
```

### 2. 模板结构设计
```markdown
# 清晰的标题
简短描述命令用途

## 分析维度/步骤
列出具体的分析框架

## 输出格式
定义期望的输出结构

请分析以下[内容类型]：
```

### 3. 内容质量要点
- **具体明确** - 避免模糊的描述
- **结构化** - 使用清晰的层级结构
- **可执行** - 提供具体的行动建议
- **专业深度** - 体现专业领域的深度理解

## 🎯 实战案例

### 案例 1: 错误日志分析
```bash
# 创建错误日志文件
echo "ERROR: Database connection failed" > db-error.log

# 使用调试命令分析
/debug-loop @db-error.log
```

### 案例 2: 代码性能审计
```bash
# 创建性能问题代码
cat > slow-code.js << 'EOF'
function processData(data) {
    for(let i=0; i<data.length; i++) {
        for(let j=0; j<data[i].length; j++) {
            // O(n²) 算法
        }
    }
}
EOF

# 使用性能审计命令
/performance-audit @slow-code.js
```

### 案例 3: 多 Agent 协作
```bash
# 营销数据分析流水线
/marketing-analysis @sales-data.csv

# 代码质量检查流水线
/code-pipeline @app.js
```

## 📝 练习作业

1. **基础练习**：创建一个 `code-review` 命令，用于基础代码质量检查

2. **进阶练习**：创建 `api-tester` 命令，专门分析 API 接口代码

3. **综合练习**：创建一个完整的 `devops-audit` 命令，包含配置检查、安全扫描、性能评估

## 🎓 总结

- 自定义命令是 Claude Code 的核心高级功能
- 好的命令 = 清晰的结构 + 专业的分析框架 + 可执行的输出
- 命令模板可以复用，提高团队效率
- 链式命令可以实现复杂的多步骤工作流

---

**下一课**: [多代理协作工作流](../lesson-03-multi-agent/README.md)