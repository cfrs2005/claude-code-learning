# Claude Code 高级技巧学习教程

> 🚀 掌握 Claude Code 的高级功能和最佳实践，提升 AI 辅助编程效率

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Advanced-blue.svg)](https://docs.anthropic.com/claude-code)

## 📖 项目介绍

这是一个系统学习 Claude Code 高级技巧的开源项目。通过实际案例和动手实践，帮助你掌握 Claude Code 的强大功能，从基础使用到高级工作流。

### 🎯 学习目标

- ✅ 掌握 `/agents` 指令系统
- ✅ 创建自定义 Slash 命令
- ✅ 实现多代理协作工作流
- ✅ 应用 Linus 式代码审查
- ✅ 构建智能分析流水线

## 📚 课程结构

### Lesson 1: Agents 指令系统
- **文件**: `lessons/lesson-01-agents/`
- **内容**: 创建和管理专门 AI 子代理
- **案例**: Linus 风格代码审查

### Lesson 2: 自定义 Slash 命令
- **文件**: `lessons/lesson-02-slash-commands/`
- **内容**: 创建可复用的命令模板
- **案例**: 调试分析、性能审计、安全扫描

### Lesson 3: 多代理协作
- **文件**: `lessons/lesson-03-multi-agent/`
- **内容**: 代理链式工作流
- **案例**: 营销数据分析与优化

### Lesson 4: 高级技巧
- **文件**: `lessons/lesson-04-advanced/`
- **内容**: Extended Thinking、Plan 模式、TDD 工作流
- **案例**: 复杂项目管理

## 🚀 快速开始

### 前置要求

- [Claude Code](https://docs.anthropic.com/claude-code) 已安装
- GitHub CLI (`gh`) 已配置
- 基础命令行知识

### 环境设置

```bash
# 克隆项目
git clone https://github.com/cfrs2005/claude-code-learning.git
cd claude-code-learning

# 复制配置文件（可选）
cp -r demos/.claude/ ./
```

### 第一个示例

```bash
# 创建第一个 agent
/agents create code-reviewer "代码审查专家"

# 使用自定义命令
/security-review demos/demo-data/insecure-code.js
```

## 📁 项目结构

```
claude-code-learning/
├── README.md                    # 项目介绍
├── LICENSE                     # MIT 协议
├── .gitignore                  # Git 忽略文件
├── lessons/                     # 课程内容
│   ├── lesson-01-agents/        # Agents 指令
│   ├── lesson-02-slash-commands/ # 自定义命令
│   ├── lesson-03-multi-agent/   # 多代理协作
│   └── lesson-04-advanced/      # 高级技巧
├── demos/                      # 完整示例
│   ├── .claude/                 # Claude 配置
│   ├── commands/               # 自定义命令
│   └── demo-data/              # 测试数据
└── docs/                       # 扩展文档
```

## 🎯 核心技巧

### 1. 🤖 Agents 系统

```bash
# 列出所有 agents
/agents list

# 创建专门 agent
/agents create marketing-analyzer "营销数据分析专家"

# 使用 agent 分析问题
marketing-analyzer 分析 @data/sales.csv
```

### 2. ⚡ 自定义命令

```bash
# 安全审查
/security-review @code/insecure.js

# 性能审计  
/performance-audit @code/slow.js

# Linus 风格审查
/linus-review @code/bad-code.js
```

### 3. 🔗 链式工作流

```bash
# 营销分析流水线
/marketing-analysis @data/sales.csv

# 代码质量流水线
/code-pipeline @code/analysis.js

# 智能全面分析
/full-analysis @any-file
```

## 📈 学习路径

### 初学者 (1-2 小时)
1. 了解 Claude Code 基础
2. 创建第一个 agent
3. 使用自定义命令
4. 完成基础案例分析

### 进阶用户 (3-5 小时)
1. 掌握多代理协作
2. 构建链式工作流
3. 应用 Linus 哲学
4. 优化工作流程

### 专家用户 (5+ 小时)
1. 设计复杂工作流
2. 集成外部工具
3. 贡献新的案例
4. 分享最佳实践

## 🛠️ 贡献指南

欢迎贡献内容！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献类型

- 📚 新的课程内容
- 💻 实用案例和脚本
- 🐛 Bug 修复
- 📖 文档改进
- 🎨 UI/UX 优化

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Anthropic](https://anthropic.com) - Claude Code
- [Linus Torvalds](https://en.wikipedia.org/wiki/Linus_Torvalds) - 代码品味哲学
- 所有贡献者和学习者

## 📞 联系方式

- 📧 Issue: [GitHub Issues](https://github.com/cfrs2005/claude-code-learning/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/cfrs2005/claude-code-learning/discussions)

---

⭐ 如果这个项目对你有帮助，请给个星标！