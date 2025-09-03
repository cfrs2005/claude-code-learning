# Lesson 1: Agents 指令系统

## 🎯 学习目标

- 理解 Claude Code 的 agents 概念
- 创建和管理专门 AI 子代理
- 实际应用：Linus 风格代码审查

## 📖 理论基础

### 什么是 Agents？

Agents 是 Claude Code 中的专门 AI 子代理，每个 agent 都有：
- **特定专业领域** (如代码审查、数据分析)
- **独立上下文窗口** (不占用主对话空间)
- **定制化系统提示** (专门的任务指令)
- **专属工具配置** (按需分配工具权限)

### Agents 的优势

1. **专业分工** - 每个 agent 专注擅长领域
2. **上下文隔离** - 避免主对话被专业内容污染
3. **可复用性** - 一次创建，多次使用
4. **团队协作** - 多个 agent 协同解决复杂问题

## 🚀 实战演练

### 步骤 1: 创建第一个 Agent

```bash
# 创建 Linus 风格代码审查 agent
/agents create linus-code-reviewer "以 Linus Torvalds 的视角审查代码质量"
```

### 步骤 2: 创建测试代码

```javascript
// bad-function.js
function badCode() { 
    var x=1; 
    for(var i=0;i<100;i++) { 
        if(i%2==0) { 
            x+=i; 
        } else { 
            x-=i; 
        } 
    } 
    return x; 
}
```

### 步骤 3: 使用 Agent 分析

```bash
# 让 linus-code-reviewer 分析代码
linus-code-reviewer 分析 @bad-function.js
```

### 预期输出示例

```
【品味评分】🔴 垃圾

【致命问题】
这代码是典型的"垃圾代码"范例。格式就像是用脚趾头敲出来的...
循环里的if/else分支完全是多余的复杂性。

【Linus式改进】
把这个特殊情况消除掉...
用数学公式代替循环...
```

## 📊 Agents 管理命令

```bash
# 列出所有 agents
/agents list

# 创建新 agent
/agents create <name> "描述"

# 删除 agent
/agents delete <name>

# 选择 agent
/agents select <name>
```

## 💡 最佳实践

### 1. Agent 命名规范
```bash
✅ 好的命名：
- linus-code-reviewer
- marketing-data-analyzer
- security-expert

❌ 避免的命名：
- agent1
- helper
- bot
```

### 2. 描述要具体
```bash
✅ 好的描述：
"以 Linus Torvalds 的风格审查代码，关注数据结构优先，消除特殊情况，保持实用主义"

❌ 模糊的描述：
"分析代码"
"帮助写代码"
```

### 3. 专注单一职责
- 每个 agent 只做一件事并做好
- 避免创建"万能 agent"
- 细分专业领域，创建多个专门 agent

## 🎯 实战案例

### 案例 1: 营销数据分析 Agent

```bash
# 创建营销数据分析专家
/agents create marketing-data-analyzer "专门分析营销数据，识别表现异常的广告，计算关键指标如CTR、转化率、ROI等"
```

### 案例 2: 广告优化 Agent

```bash
# 创建广告优化专家
/agents create ad-optimizer "基于数据分析结果，为表现差的广告生成优化建议和新的变体方案"
```

### 案例 3: 安全审查 Agent

```bash
# 创建安全专家
/agents create security-expert "识别代码中的安全漏洞，包括SQL注入、XSS、权限控制等问题"
```

## 🔄 进阶技巧

### 多 Agent 协作

```bash
# 让多个 agent 协作处理同一问题
marketing-data-analyzer 分析 @sales-data.csv
# 基于分析结果
ad-optimizer 优化 @analysis-result
```

### Agent 链式调用

```bash
# 创建链式工作流 agent
/agents create workflow-manager "协调多个专门 agents 的执行，确保信息正确传递"
```

## 📝 练习作业

1. **基础练习**：创建一个 "python-expert" agent，专门分析 Python 代码

2. **进阶练习**：创建 "refactoring-specialist" agent，专注于代码重构

3. **综合练习**：创建至少 3 个不同领域的 agents，并让它们协作解决一个复杂问题

## 🎓 总结

- Agents 是 Claude Code 的核心高级功能
- 专业分工让 AI 更高效、更精准
- 好的 agent = 明确的领域 + 具体的描述
- 多 agent 协作可以解决复杂问题

---

**下一课**: [自定义 Slash 命令](../lesson-02-slash-commands/README.md)