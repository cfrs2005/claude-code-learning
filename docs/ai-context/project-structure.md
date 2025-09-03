# 项目结构模板

本文档提供了一个完整技术栈和文件树结构的文档模板。**AI 智能体必须先阅读此文件以了解项目组织，然后再进行任何更改。**

## 技术栈模板

### 后端技术
记录你的后端技术选择：
- **[语言] [版本]** 与 **[包管理器]** - 依赖管理和打包
- **[Web框架] [版本]** - 带特定功能的 Web 框架（异步、类型提示等）
- **[服务器] [版本]** - 应用服务器配置
- **[配置] [版本]** - 配置管理方法

示例：
```
- Python 3.11+ 与 Poetry - 依赖管理和打包
- FastAPI 0.115.0+ - 带类型提示和异步支持的 Web 框架
- Uvicorn 0.32.0+ - 带标准扩展的 ASGI 服务器
- Pydantic Settings 2.5.2+ - 带类型验证的配置管理
```

### 集成服务与 API
记录外部服务和集成：
- **[服务名] [API/SDK版本]** - 用途和使用模式
- **[AI服务] [版本]** - AI/ML 服务集成详情
- **[数据库] [版本]** - 数据存储和管理
- **[监控] [版本]** - 可观测性和日志

### 实时通信
记录实时功能：
- **[WebSocket库]** - 实时通信模式
- **[HTTP客户端]** - 异步 HTTP 通信
- **[消息队列]** - 事件处理（如适用）

### 开发与质量工具
记录开发工具链：
- **[格式化器] [版本]** - 代码格式化
- **[代码检查器] [版本]** - 代码质量和代码检查
- **[类型检查器] [版本]** - 静态类型检查
- **[测试框架] [版本]** - 测试方法
- **[任务运行器]** - 构建自动化和任务编排

### 前端技术（如适用）
记录前端技术栈：
- **[语言] [版本]** - 前端开发语言
- **[框架] [版本]** - UI 框架
- **[构建工具] [版本]** - 开发和构建工具
- **[部署] [版本]** - 部署和托管方法

### 未来技术
记录计划的技术添加：
- **[计划技术]** - 未来集成计划
- **[平台]** - 目标平台扩展
- **[服务]** - 计划的服务集成

## 完整项目结构模板

```
[项目名称]/
├── README.md                           # 项目概览和设置
├── CLAUDE.md                           # 主 AI 上下文文件
├── [构建文件]                          # 构建配置（Makefile、package.json 等）
├── .gitignore                          # Git 忽略模式
├── .[IDE配置]/                         # IDE 工作区配置
│   ├── settings.[ext]                  # IDE 设置
│   ├── extensions.[ext]                # 推荐扩展
│   └── launch.[ext]                    # 调试配置
├── [后端目录]/                         # 后端应用
│   ├── CONTEXT.md                      # 后端特定 AI 上下文
│   ├── src/                            # 源代码
│   │   ├── config/                     # 配置管理
│   │   │   └── settings.[ext]          # 应用设置
│   │   ├── core/                       # 核心业务逻辑
│   │   │   ├── CONTEXT.md              # 核心逻辑模式
│   │   │   ├── services/               # 业务服务
│   │   │   │   ├── [service1].[ext]    # 服务实现
│   │   │   │   └── [service2].[ext]
│   │   │   ├── models/                 # 数据模型
│   │   │   │   ├── [model1].[ext]      # 模型定义
│   │   │   │   └── [model2].[ext]
│   │   │   └── utils/                  # 工具函数
│   │   │       ├── logging.[ext]       # 结构化日志
│   │   │       ├── validation.[ext]    # 输入验证
│   │   │       └── helpers.[ext]       # 辅助函数
│   │   ├── api/                        # API 层
│   │   │   ├── CONTEXT.md              # API 模式和约定
│   │   │   ├── routes/                 # API 路由定义
│   │   │   │   ├── [resource1].[ext]   # 资源特定路由
│   │   │   │   └── [resource2].[ext]
│   │   │   ├── middleware/             # API 中间件
│   │   │   │   ├── auth.[ext]          # 认证中间件
│   │   │   │   ├── logging.[ext]       # 请求日志
│   │   │   │   └── validation.[ext]    # 请求验证
│   │   │   └── schemas/                # 请求/响应模式
│   │   │       ├── [schema1].[ext]     # 数据模式
│   │   │       └── [schema2].[ext]
│   │   └── integrations/               # 外部服务集成
│   │       ├── CONTEXT.md              # 集成模式
│   │       ├── [service1]/             # 服务特定集成
│   │       │   ├── client.[ext]        # API 客户端
│   │       │   ├── models.[ext]        # 集成模型
│   │       │   └── handlers.[ext]      # 响应处理器
│   │       └── [service2]/
│   ├── tests/                          # 测试套件
│   │   ├── unit/                       # 单元测试
│   │   ├── integration/                # 集成测试
│   │   └── fixtures/                   # 测试夹具和数据
│   ├── [包文件]                        # 包配置
│   └── [环境文件]                      # 环境配置
├── [前端目录]/                         # 前端应用（如适用）
│   ├── CONTEXT.md                      # 前端特定 AI 上下文
│   ├── src/                            # 源代码
│   │   ├── components/                 # UI 组件
│   │   │   ├── CONTEXT.md              # 组件模式
│   │   │   ├── common/                 # 共享组件
│   │   │   └── [feature]/              # 功能特定组件
│   │   ├── pages/                      # 页面组件/路由
│   │   │   ├── [page1].[ext]           # 页面实现
│   │   │   └── [page2].[ext]
│   │   ├── stores/                     # 状态管理
│   │   │   ├── CONTEXT.md              # 状态管理模式
│   │   │   ├── [store1].[ext]          # 存储实现
│   │   │   └── [store2].[ext]
│   │   ├── api/                        # API 客户端层
│   │   │   ├── CONTEXT.md              # 客户端模式
│   │   │   ├── client.[ext]            # HTTP 客户端设置
│   │   │   └── endpoints/              # API 端点定义
│   │   ├── utils/                      # 工具函数
│   │   │   ├── logging.[ext]           # 客户端日志
│   │   │   ├── validation.[ext]        # 表单验证
│   │   │   └── helpers.[ext]           # 辅助函数
│   │   └── assets/                     # 静态资源
│   ├── tests/                          # 前端测试
│   ├── [构建配置]                      # 构建配置
│   └── [包文件]                        # 包配置
├── docs/                               # 文档
│   ├── ai-context/                     # AI特定文档
│   │   ├── project-structure.md        # 此文件
│   │   ├── docs-overview.md            # 文档架构
│   │   ├── system-integration.md       # 集成模式
│   │   ├── deployment-infrastructure.md # 基础设施文档
│   │   └── handoff.md                  # 任务管理
│   ├── api/                            # API 文档
│   ├── deployment/                     # 部署指南
│   └── development/                    # 开发指南
├── scripts/                            # 自动化脚本
│   ├── setup.[ext]                     # 环境设置
│   ├── deploy.[ext]                    # 部署脚本
│   └── maintenance/                    # 维护脚本
├── [基础设施目录]/                     # 基础设施即代码（如适用）
│   ├── [提供商]/                       # 云提供商配置
│   ├── docker/                         # 容器配置
│   └── monitoring/                     # 监控和告警
└── [配置文件]                          # 根级配置文件
```

---

*此模板为项目结构文档提供了全面基础。根据你的特定技术栈、架构决策和组织要求进行调整。*