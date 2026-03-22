# Agent 开发（Harness 工程）学习计划

> **核心理念**：模型是 Agent，代码是 Harness。你学习的是如何构建 Harness。

---

## 学习路线总览

```
Phase 1: 循环基础        Phase 2: 规划与知识
================        ====================
s01 Agent Loop    ──►   s03 TodoWrite
      │                       │
      ▼                       ▼
s02 Tool Use      ◄─┘   s04 Subagents
                              │
                              ▼
                         s05 Skills
                              │
                              ▼
                         s06 Context Compact

Phase 3: 持久化          Phase 4: 团队协作
================        ====================
s07 Task System   ──►   s09 Agent Teams
      │                       │
      ▼                       ▼
s08 Background           s10 Team Protocols
   Tasks                       │
                              ▼
                         s11 Autonomous Agents
                              │
                              ▼
                         s12 Worktree Isolation
```

---

## Phase 1: 循环基础

### s01 - The Agent Loop（智能体循环）

**格言**：*"一个循环 + Bash = 一个智能体"*

**核心概念**：
- [ ] `while True` 循环
- [ ] `stop_reason` 判断（`tool_use` vs 结束）
- [ ] 工具调用 → 结果返回 → 继续循环

**代码路径**：`agents/s01_agent_loop.py`

**文档路径**：`docs/zh/s01-the-agent-loop.md`

**练习任务**：
1. [ ] 让 Agent 创建一个 `hello.py` 文件
2. [ ] 让 Agent 列出当前目录的 Python 文件
3. [ ] 让 Agent 查看 git 分支

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s02 - Tool Use（工具使用）

**格言**：*"添加工具就是添加一个处理器"*

**核心概念**：
- [ ] `TOOL_HANDLERS` 分发映射
- [ ] 工具定义（name, description, input_schema）
- [ ] 路由模式：`handler = TOOL_HANDLERS[block.name]`

**新增工具**：`bash` + `read_file` + `write_file` + `edit_file`

**代码路径**：`agents/s02_tool_use.py`

**文档路径**：`docs/zh/s02-tool-use.md`

**练习任务**：
1. [ ] 让 Agent 读取一个文件并总结内容
2. [ ] 让 Agent 修改文件中的某段代码
3. [ ] 观察 Agent 如何选择正确的工具

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

## Phase 2: 规划与知识

### s03 - TodoWrite（待办写入）

**格言**：*"没有计划的 Agent 走哪算哪"*

**核心概念**：
- [ ] `TodoManager` 状态管理
- [ ] 只允许一个任务 `in_progress`
- [ ] Nag reminder：3轮未更新则自动提醒

**代码路径**：`agents/s03_todo_write.py`

**文档路径**：`docs/zh/s03-todo-write.md`

**练习任务**：
1. [ ] 让 Agent 重构一个文件（添加类型提示、docstring、main guard）
2. [ ] 观察它如何分解任务并逐一完成

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s04 - Subagents（子智能体）

**格言**：*"大任务拆小，每个小任务干净的上下文"*

**核心概念**：
- [ ] 子智能体拥有独立的 `messages[]`
- [ ] 只返回摘要，不污染父上下文
- [ ] 防止上下文膨胀

**代码路径**：`agents/s04_subagent.py`

**文档路径**：`docs/zh/s04-subagent.md`

**练习任务**：
1. [ ] 让 Agent 用子任务查找项目使用的测试框架
2. [ ] 让 Agent 委托子任务读取所有 .py 文件并总结

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s05 - Skills（技能加载）

**格言**：*"需要时再加载知识，而不是一开始就加载"*

**核心概念**：
- [ ] `SKILL.md` 文件格式
- [ ] 通过 `tool_result` 注入，而非 system prompt
- [ ] 动态加载，减少初始上下文占用

**代码路径**：`agents/s05_skill_loading.py`

**文档路径**：`docs/zh/s05-skill-loading.md`

**练习任务**：
1. [ ] 创建一个自定义 skill 文件
2. [ ] 让 Agent 在需要时加载该 skill

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s06 - Context Compact（上下文压缩）

**格言**：*"上下文会填满，你需要腾出空间"*

**核心概念**：
- [ ] 三层压缩策略
- [ ] 保留关键信息，丢弃冗余
- [ ] 允许长时间运行的会话

**代码路径**：`agents/s06_context_compact.py`

**文档路径**：`docs/zh/s06-context-compact.md`

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

## Phase 3: 持久化

### s07 - Task System（任务系统）

**格言**：*"大目标拆成小任务，排好序，记在磁盘上"*

**核心概念**：
- [ ] `.tasks/` 目录存储 JSON 文件
- [ ] `blockedBy` / `blocks` 依赖关系
- [ ] DAG（有向无环图）任务结构
- [ ] 状态：`pending` → `in_progress` → `completed`

**代码路径**：`agents/s07_task_system.py`

**文档路径**：`docs/zh/s07-task-system.md`

**练习任务**：
1. [ ] 创建有依赖关系的任务链
2. [ ] 完成前置任务，观察后续任务解锁

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s08 - Background Tasks（后台任务）

**格言**：*"慢操作后台跑，Agent 继续思考"*

**核心概念**：
- [ ] Daemon 线程执行长时间命令
- [ ] 通知队列注入结果
- [ ] Agent 不阻塞等待

**代码路径**：`agents/s08_background_tasks.py`

**文档路径**：`docs/zh/s08-background-tasks.md`

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

## Phase 4: 团队协作

### s09 - Agent Teams（智能体团队）

**格言**：*"任务太大，分给队友"*

**核心概念**：
- [ ] `TeammateManager` 管理团队名册
- [ ] JSONL 格式的邮箱通信
- [ ] 队友生命周期：`spawn` → `working` → `idle`

**代码路径**：`agents/s09_agent_teams.py`

**文档路径**：`docs/zh/s09-agent-teams.md`

**练习任务**：
1. [ ] 生成 alice（coder）和 bob（tester）
2. [ ] 让 alice 发送消息给 bob
3. [ ] 广播状态更新

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s10 - Team Protocols（团队协议）

**格言**：*"队友需要共享的通信规则"*

**核心概念**：
- [ ] 关机握手协议
- [ ] 计划审批 FSM
- [ ] 消息类型定义

**代码路径**：`agents/s10_team_protocols.py`

**文档路径**：`docs/zh/s10-team-protocols.md`

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s11 - Autonomous Agents（自治智能体）

**格言**：*"队友自己看看板，有活就认领"*

**核心概念**：
- [ ] IDLE 阶段轮询
- [ ] 自动扫描未认领任务
- [ ] 身份重注入（压缩后恢复记忆）

**代码路径**：`agents/s11_autonomous_agents.py`

**文档路径**：`docs/zh/s11-autonomous-agents.md`

**练习任务**：
1. [ ] 创建多个任务，生成队友，观察自动认领
2. [ ] 创建有依赖的任务，观察队友遵守阻塞顺序

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

### s12 - Worktree Isolation（Worktree 隔离）

**格言**：*"各干各的目录，互不干扰"*

**核心概念**：
- [ ] 任务与 git worktree 绑定
- [ ] 独立的执行目录
- [ ] 事件流记录生命周期

**代码路径**：`agents/s12_worktree_task_isolation.py`

**文档路径**：`docs/zh/s12-worktree-task-isolation.md`

**练习任务**：
1. [ ] 创建任务并为任务创建 worktree
2. [ ] 在 worktree 中执行命令
3. [ ] 保留/删除 worktree

**学习笔记**：
```
（在这里记录你的学习心得）
```

---

## 学习进度总览

| 阶段 | Session | 状态 | 完成日期 |
|------|---------|------|----------|
| Phase 1 | s01 Agent Loop | ⬜ 未开始 | |
| Phase 1 | s02 Tool Use | ⬜ 未开始 | |
| Phase 2 | s03 TodoWrite | ⬜ 未开始 | |
| Phase 2 | s04 Subagents | ⬜ 未开始 | |
| Phase 2 | s05 Skills | ⬜ 未开始 | |
| Phase 2 | s06 Context Compact | ⬜ 未开始 | |
| Phase 3 | s07 Task System | ⬜ 未开始 | |
| Phase 3 | s08 Background Tasks | ⬜ 未开始 | |
| Phase 4 | s09 Agent Teams | ⬜ 未开始 | |
| Phase 4 | s10 Team Protocols | ⬜ 未开始 | |
| Phase 4 | s11 Autonomous Agents | ⬜ 未开始 | |
| Phase 4 | s12 Worktree Isolation | ⬜ 未开始 | |

**图例**：⬜ 未开始 | 🔄 进行中 | ✅ 已完成

---

## 环境准备检查清单

- [ ] 克隆项目
- [ ] 安装依赖：`pip install -r requirements.txt`
- [ ] 配置 API：复制 `.env.example` 为 `.env` 并填入 API Key
- [ ] 验证环境：`python agents/s01_agent_loop.py`

---

## 学习笔记区

### 整体心得

```
（学习完成后在这里记录你的整体感悟）
```

### 遇到的问题与解决方案

```
（记录学习过程中遇到的问题和解决方法）
```

### 自定义练习

```
（记录你自己设计的练习和实验）
```
