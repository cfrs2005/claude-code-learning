# Lesson 9: 实用工作流与高级配置管理

## 🎯 学习目标

- 掌握 Kiro 规范驱动开发工作流
- 学习 GitHub 集成和 Issue 修复流程
- 理解多模型提供商配置和代理设置
- 掌握实用的高级思考和分析命令

## 📖 理论基础

### 为什么需要实用工作流？

feiskyer/claude-code-settings 项目展示了 Claude Code 在实际开发中的高级应用。这些工作流解决了：

1. **开发流程标准化** - Kiro 工作流确保从需求到实现的完整流程
2. **GitHub 集成** - 自动化的 Issue 修复和 PR 审查流程
3. **多模型支持** - 灵活的模型提供商配置（Copilot、LiteLLM、DeepSeek 等）
4. **增强思考能力** - 系统化的深度分析和反思工具

### 核心设计原则

#### 1. 规范驱动开发 (Spec-Driven Development)
```
需求 → 设计 → 任务 → 实现 → 测试
```

#### 2. 增强思考能力 (Enhanced Thinking)
```
基础思考 → 深度分析 → 全面评估 → 反思改进
```

#### 3. 自动化集成 (Automated Integration)
```
GitHub Issues → 自动修复 → PR 创建 → 代码审查
```

## 🚀 实战演练

### 步骤 1: Kiro 规范驱动开发工作流

Kiro 工作流是一个完整的系统化开发流程，从想法到实现的全生命周期管理。

#### 1.1 创建功能规范

使用 `/kiro:spec [feature]` 创建完整的功能规范：

```markdown
# Kiro Spec Creation Workflow

## Phase 1: 需求收集
- 生成 EARS 格式的初始需求
- 迭代完善直到需求完整准确
- 创建 `.kiro/specs/{feature_name}/requirements.md`

## Phase 2: 设计文档
- 基于需求进行必要的研究
- 创建综合设计文档
- 包含架构、组件、数据模型等
- 创建 `.kiro/specs/{feature_name}/design.md`

## Phase 3: 任务计划
- 将设计转化为可执行的任务清单
- 每个任务都是具体的编码步骤
- 创建 `.kiro/specs/{feature_name}/tasks.md`

## Phase 4: 执行实现
- 按任务清单逐步执行
- 每个任务都经过测试验证
- 增量式开发，确保质量
```

#### 1.2 实现示例命令

创建 `.claude/commands/kiro-spec.md`:

```markdown
---
description: 创建完整的功能规范，从需求到实现计划
argument-hint: [功能名称或初步想法]
---

# Kiro 功能规范创建

你正在帮助用户将粗略的功能想法转化为详细的设计文档和实施计划。

## 工作流程

### 1. 需求收集

首先，基于功能想法生成初始需求集，然后与用户迭代完善直到需求完整准确。

**约束条件:**

- 必须创建 `.kiro/specs/{feature_name}/requirements.md` 文件
- 必须基于用户的初步想法生成初始需求文档
- 需求文档格式必须包含：
  - 清晰的介绍部分总结功能
  - 分层编号的需求列表，每个包含：
    - 格式为"As a [role], I want [feature], so that [benefit]"的用户故事
    - EARS 格式的验收标准编号列表

### 2. 设计文档

用户批准需求后，基于功能需求开发综合设计文档，在设计过程中进行必要的研究。

**约束条件:**

- 必须创建 `.kiro/specs/{feature_name}/design.md` 文件
- 必须识别基于功能需求需要研究的领域
- 必须在设计文档中包含以下部分：
  - 概述
  - 架构
  - 组件和接口
  - 数据模型
  - 错误处理
  - 测试策略

### 3. 任务清单

用户批准设计后，基于需求和设计创建可操作的实现计划。

**约束条件:**

- 必须创建 `.kiro/specs/{feature_name}/tasks.md` 文件
- 必须将设计转化为一系列代码生成 LLM 的提示
- 优先考虑最佳实践、增量进展和早期测试
- 格式为带复选框的编号列表，最多两层层次结构

请分析以下功能想法：
```
```
```

### 步骤 2: 增强思考能力命令

创建 `.claude/commands/think-harder.md`:

```markdown
---
description: 对复杂问题进行增强的分析思考
argument-hint: [问题或疑问]
---

# 深度思考命令

对以下问题进行深度分析思考：**$ARGUMENTS**

## 深度分析协议

应用系统化推理方法：

### 1. 问题澄清

- 定义核心问题并识别隐含假设
- 建立范围、约束和成功标准
- 梳理潜在的模糊性和多种解释

### 2. 多维度分析

- **结构分解**: 分解为基本组件和依赖关系
- **利益相关者视角**: 考虑所有受影响方的观点
- **时间分析**: 检查短期 vs 长期影响
- **因果推理**: 映射因果关系和反馈循环
- **情境因素**: 评估环境、文化和情境影响

### 3. 批判性评估

- 挑战你的初始假设并识别认知偏见
- 生成和评估替代假设或解决方案
- 进行事前分析：可能出错的地方及原因
- 考虑每个方法的机会成本和权衡
- 评估置信度水平和不确定性来源

### 4. 综合与整合

- 跨不同领域和学科连接见解
- 识别组件交互中的涌现属性
- 调和明显的矛盾或悖论
- 开发关于问题解决过程本身的元见解

## 输出结构

按此格式呈现你的分析：

1. **问题重构**: 你如何理解核心问题
2. **关键见解**: 分析中最重要的发现
3. **推理链条**: 逐步的逻辑进展
4. **考虑的替代方案**: 评估的不同方法
5. **不确定性**: 你不知道什么以及为什么重要
6. **可操作建议**: 具体的、可实施的下一步

要彻底但简洁。展示你的推理过程，而不仅仅是结论。
```

### 步骤 3: GitHub 集成命令

创建 `.claude/commands/gh-fix-issue.md`:

```markdown
---
description: 修复 GitHub Issue
argument-hint: [issue-number]
allowed-tools: Write, Read, LS, Glob, Grep, Bash(gh:*), Bash(git:*)
---

请按照以下步骤分析和修复 GitHub Issue $ARGUMENTS：

## 计划

1. 使用 'gh issue view' 获取 Issue 详情
2. 理解 Issue 中描述的问题
3. 必要时提出澄清问题
4. 了解此 Issue 的背景
   - 搜索相关的先前思考
   - 搜索 PR 以查找此 Issue 的历史记录
   - 搜索代码库中的相关文件
5. 深度思考如何将 Issue 分解为一系列小的、可管理的任务
6. 在新的便签中记录你的计划
   - 在文件名中包含 Issue 名称
   - 在便签中包含 Issue 链接

## 创建

- 为 Issue 创建新分支
- 根据你的计划以小的、可管理的步骤解决问题
- 每步后提交更改

## 测试

- 如果你对 UI 进行了更改且 puppeteer 在工具列表中，使用 puppeteer 测试更改
- 编写单元测试描述代码的预期行为
- 运行完整测试套件确保没有破坏任何内容
- 如果测试失败，修复它们
- 在进行下一步之前确保所有测试通过

## 开启 Pull Request

- 开启 PR 并请求审查

记住对所有 GitHub 相关任务使用 GitHub CLI ('gh')。
```

### 步骤 4: 高级配置管理

#### 4.1 多模型提供商配置

基于 feiskyer 项目，创建灵活的模型配置：

创建 `.claude/settings/` 目录和不同的配置文件：

**Copilot 配置 (settings/copilot-settings.json)**:
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "api_base": "http://localhost:4141/v1",
  "permissions": {
    "allow": [
      "Read",
      "Write", 
      "LS",
      "Grep",
      "Bash(npm:*)",
      "Bash(gh:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "WebFetch",
      "Bash(curl:*)"
    ]
  }
}
```

**LiteLLM 配置 (settings/litellm-settings.json)**:
```json
{
  "model": "claude-3-5-sonnet-20241022", 
  "api_base": "http://localhost:4000",
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "LS", 
      "Grep",
      "Bash(npm:*)",
      "Bash(python:*)"
    ],
    "deny": [
      "WebFetch"
    ]
  }
}
```

#### 4.2 环境感知配置

创建 `.claude/settings-switcher.md` 命令：

```markdown
---
description: 根据项目类型和需求自动切换最佳配置
argument-hint: [项目类型或需求]
---

# 配置切换器

根据项目类型和需求自动选择最佳 Claude Code 配置。

## 项目类型识别

### 前端项目
- 检测到: package.json + React/Vue/Angular
- 推荐配置: copilot-settings.json
- 理由: 更好的代码补全和前端优化

### 后端项目  
- 检测到: requirements.txt + Django/Flask/FastAPI
- 推荐配置: litellm-settings.json
- 理由: 更好的 Python 支持和后端优化

### 全栈项目
- 检测到: 前端 + 后端文件
- 推荐配置: copilot-settings.json
- 理由: 综合支持和更好的代码生成

### 数据科学项目
- 检测到: .ipynb + pandas/numpy
- 推荐配置: litellm-settings.json  
- 理由: 更好的数据科学模型支持

## 自动切换逻辑

### 检测命令
```bash
# 检测项目类型
if [ -f "package.json" ] && grep -q "react\|vue\|angular" package.json; then
    echo "frontend"
elif [ -f "requirements.txt" ] && grep -q "django\|flask\|fastapi" requirements.txt; then
    echo "backend"  
elif [ -f "package.json" ] && [ -f "requirements.txt" ]; then
    echo "fullstack"
elif ls *.ipynb 1> /dev/null 2>&1; then
    echo "datascience"
else
    echo "general"
fi
```

### 配置应用
```bash
# 应用配置
case $PROJECT_TYPE in
    frontend)
        cp .claude/settings/copilot-settings.json .claude/settings.json
        ;;
    backend)
        cp .claude/settings/litellm-settings.json .claude/settings.json
        ;;
    fullstack)
        cp .claude/settings/copilot-settings.json .claude/settings.json
        ;;
    datascience)
        cp .claude/settings/litellm-settings.json .claude/settings.json
        ;;
    *)
        cp .claude/settings/default-settings.json .claude/settings.json
        ;;
esac
```

请分析当前项目并推荐最佳配置。
```

## 📊 高级工作流模式

### 1. 完整的开发工作流

```bash
# 阶段 1: 需求分析
/kiro:spec "用户认证系统"

# 阶段 2: 架构设计  
/kiro:design "用户认证系统"

# 阶段 3: 任务规划
/kiro:task "用户认证系统"

# 阶段 4: 增强思考
/think-harder "认证系统的安全性和可扩展性"

# 阶段 5: 逐步执行
/kiro:execute "创建用户模型"
/kiro:execute "实现 JWT 认证"
/kiro:execute "添加权限控制"

# 阶段 6: GitHub 集成
/gh:fix-issue 123
```

### 2. 团队协作工作流

```bash
# 开发者 A: 功能开发
/kiro:spec "购物车功能"
/kiro:design "购物车功能" 
/kiro:task "购物车功能"

# 开发者 B: 代码审查
/pr-reviewer 审查分支 "feature/shopping-cart"

# 开发者 C: Issue 修复
/gh:fix-issue 456

# 团队: 反思改进
/reflection-harder
```

### 3. 学习和改进工作流

```bash
# 开发阶段
/kiro:execute "实现核心功能"

# 思考阶段
/think-harder "当前实现的问题和改进空间"

# 突破记录
/eureka "发现更高效的数据结构"

# 反思总结
/reflection "本周开发经验和教训"
```

## 💡 实用配置示例

### 1. 项目初始化脚本

创建 `.claude/init-project.sh`:

```bash
#!/bin/bash
# 项目初始化脚本

echo "🚀 初始化 Claude Code 项目..."

# 检测项目类型
if [ -f "package.json" ]; then
    if grep -q "react\|vue\|angular" package.json; then
        PROJECT_TYPE="frontend"
    else
        PROJECT_TYPE="nodejs"
    fi
elif [ -f "requirements.txt" ]; then
    if grep -q "django\|flask\|fastapi" requirements.txt; then
        PROJECT_TYPE="backend"
    else
        PROJECT_TYPE="python"
    fi
else
    PROJECT_TYPE="general"
fi

echo "📁 检测到项目类型: $PROJECT_TYPE"

# 创建目录结构
mkdir -p .claude/{agents,commands,settings,hooks}
mkdir -p .kiro/specs

# 复制基础配置
case $PROJECT_TYPE in
    frontend)
        cp templates/frontend-settings.json .claude/settings.json
        ;;
    backend)
        cp templates/backend-settings.json .claude/settings.json
        ;;
    *)
        cp templates/default-settings.json .claude/settings.json
        ;;
esac

# 复制常用命令
cp templates/common-commands/* .claude/commands/

# 初始化 Git 钩子
cp templates/hooks/* .claude/hooks/

echo "✅ 项目初始化完成!"
echo "📋 下一步:"
echo "   1. 检查 .claude/settings.json 配置"
echo "   2. 运行 /kiro:spec 开始第一个功能"
echo "   3. 使用 /think-harder 进行深度思考"
```

### 2. 自动化质量检查

创建 `.claude/hooks/quality-check.sh`:

```bash
#!/bin/bash
# 质量检查钩子

set -e

echo "🔍 执行质量检查..."

# 1. 代码格式检查
if command -v ruff &> /dev/null; then
    echo "📝 运行 ruff 检查..."
    ruff check .
    ruff format --check .
fi

# 2. 类型检查
if command -v mypy &> /dev/null; then
    echo "🔬 运行类型检查..."
    mypy .
fi

# 3. 测试检查
if command -v pytest &> /dev/null; then
    echo "🧪 运行测试..."
    pytest
fi

# 4. 安全检查
if command -v bandit &> /dev/null; then
    echo "🔒 运行安全检查..."
    bandit -r .
fi

echo "✅ 质量检查通过"
```

## 🎯 实战案例

### 案例 1: 电商功能开发

**需求**: 开发用户认证、产品目录和购物车功能

**执行流程**:

1. **需求规范**
```bash
/kiro:spec "用户认证和购物车系统"
```

2. **架构设计**
```bash
/kiro:design "微服务架构的电商系统"
```

3. **任务分解**
```bash
/kiro:task "认证服务和产品服务"
```

4. **深度思考**
```bash
/think-harder "分布式会话管理的最佳实践"
```

5. **逐步实现**
```bash
/kiro:execute "创建用户服务"
/kiro:execute "实现 JWT 认证"
/kiro:execute "创建产品目录 API"
```

### 案例 2: 开源项目维护

**需求**: 修复开源项目中的 Issue 和改进代码质量

**执行流程**:

1. **Issue 分析**
```bash
/gh:fix-issue 42
```

2. **代码审查**
```bash
/pr-reviewer 分析 PR #123
```

3. **性能优化**
```bash
/think-ultra "数据库查询优化策略"
```

4. **文档更新**
```bash
/documentation-specialist "更新 API 文档"
```

## 📝 练习作业

1. **Kiro 工作流实践**: 使用 Kiro 工作流开发一个小功能，从需求到实现的完整流程。

2. **GitHub 集成**: 为你的项目设置 GitHub 集成，实现 Issue 自动修复。

3. **配置管理**: 创建多环境配置，支持不同的开发场景。

4. **团队协作**: 设计一个适合团队的工作流，包含角色分工和协作规范。

## 🎓 总结

### 关键学习要点

1. **规范驱动开发** - Kiro 工作流确保从需求到实现的完整性和一致性
2. **增强思考能力** - 系统化的深度分析工具提升问题解决质量
3. **自动化集成** - GitHub 集成实现开发流程的自动化
4. **灵活配置** - 多模型支持和环境感知配置适应不同需求
5. **实用工具** - 质量检查、项目初始化等工具提升开发效率

### 实际应用价值

- **开发效率** - 标准化工作流减少重复劳动
- **代码质量** - 系统化的质量保证流程
- **团队协作** - 清晰的分工和协作规范
- **技术栈灵活** - 支持多种模型和开发环境

---

**课程完成**: 恭喜！你已经掌握了 Claude Code 的实用工作流和高级配置管理。这些技能将帮助你在实际项目中建立高效、标准化的 AI 辅助开发流程。