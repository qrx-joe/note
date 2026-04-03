# Momerandum 备忘录应用改进建议

## 项目概述

Momerandum 是一个基于 Flask + JSON 的轻量级备忘录应用，提供基础的 CRUD、标签管理、搜索筛选等功能。

---

## 一、现状分析

### 1.1 当前功能

| 功能 | 状态 |
|------|------|
| 添加备忘录 | ✅ 已实现 |
| 编辑备忘录 | ✅ 已实现 |
| 删除备忘录 | ✅ 已实现 |
| 标签系统 | ✅ 已实现 |
| 置顶功能 | ✅ 已实现 |
| 搜索功能 | ✅ 已实现 |
| 标签筛选 | ✅ 已实现 |
| 分页 | ✅ 已实现 |

### 1.2 技术栈

- 后端：Flask (Python)
- 前端：HTML + CSS (原生)
- 数据存储：JSON 文件
- 部署：本地运行

### 1.3 存在不足

1. **UI 朴素** - 缺乏现代感和交互细节
2. **内容无格式** - 纯文本，无 Markdown/富文本
3. **功能单一** - 无分类/文件夹/归档
4. **移动端体验一般** - 响应式设计不完善
5. **数据安全** - JSON 文件读写无版本控制

---

## 二、改进建议

### 2.1 UI/UX 改进（高优先级）

#### 2.1.1 布局优化

参考 Notion/Obsidian 的三栏布局：

```
┌──────────┬──────────────┬─────────────┐
│  侧边栏  │   备忘录列表  │   详细内容   │
│ (导航)   │  (卡片展示)  │  (编辑器)   │
└──────────┴──────────────┴─────────────┘
```

**侧边栏功能：**
- 所有备忘录
- 标签列表（自动生成）
- 收藏/置顶
- 回收站
- 设置

#### 2.1.2 视觉设计

| 改进点 | 说明 |
|--------|------|
| 深色模式 | 支持手动/自动切换 |
| 卡片hover动效 | 轻微上浮 + 阴影加深 |
| 过渡动画 | 页面切换、弹框出现使用 ease-out |
| 图标系统 | 使用 Feather Icons 或 Heroicons |
| 字体优化 | 考虑 Inter、Noto Sans SC |

#### 2.1.3 移动端适配

- 底部导航栏替代顶部导航
- 侧边栏改为抽屉式
- 卡片列表改为单列

---

### 2.2 功能增强（中优先级）

#### 2.2.1 Markdown 支持

集成 Markdown 编辑器（推荐：SimpleMDE 或 ByteMD）：

```javascript
// 示例：使用 SimpleMDE
var simplemde = new SimpleMDE({
    element: document.getElementById('content'),
    spellChecker: false,
    autosave: true,
    promptURLs: true,
    toolbar: ["bold", "italic", "heading", "|", "code", "quote", "unordered-list", "|", "link", "image", "|", "preview"]
});
```

**渲染展示：**
- 使用 marked.js 解析 Markdown
- 代码高亮：highlight.js
- 数学公式：KaTeX

#### 2.2.2 快速记录

首页添加浮动输入框：

```html
<div class="quick-add">
    <input type="text" placeholder="快速记录..." autofocus>
    <button>添加</button>
</div>
```

支持回车直接提交，无需跳转页面。

#### 2.2.3 回收站功能

- 删除时进入回收站而非直接删除
- 回收站可查看、恢复、彻底删除
- 30天后自动清理（可选）

#### 2.2.4 数据导出

支持导出格式：
- JSON（完整备份）
- Markdown（单篇/批量）
- PDF（打印友好）

---

### 2.3 技术升级（低优先级）

#### 2.3.1 数据库迁移

从 JSON 迁移到 SQLite：

```python
# 使用 SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Memo(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500))  # 存储为逗号分隔
    pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)  # 软删除
```

**优势：**
- 并发读写更稳定
- 支持事务回滚
- 查询性能更好

#### 2.3.2 编辑器集成

可选方案：

| 编辑器 | 特点 | 难度 |
|--------|------|------|
| SimpleMDE | 轻量、易用 | ⭐ |
| ByteMD | 支持实时预览 | ⭐⭐ |
| TinyMCE | 功能强大、可视化 | ⭐⭐⭐ |
| Tiptap | Vue/React 友好 | ⭐⭐⭐ |

#### 2.3.3 前端框架

如有条件，可引入轻量框架：

- **Alpine.js** - 无需构建，适合简单交互
- **Vue 3 (CDN)** - 响应式数据绑定
- **htm** - 轻量级替代方案

---

## 三、实施路线图

### Phase 1：UI 改版（预计 2-3 天）

- [ ] 重构布局为三栏结构
- [ ] 添加深色模式
- [ ] 优化卡片样式和动效
- [ ] 移动端底部导航

### Phase 2：功能增强（预计 3-5 天）

- [ ] 集成 Markdown 编辑器
- [ ] 实现快速记录入口
- [ ] 添加回收站功能
- [ ] 实现数据导出

### Phase 3：技术升级（预计 5-7 天）

- [ ] 迁移至 SQLite
- [ ] 添加数据版本/备份
- [ ] 性能优化
- [ ] 测试和部署

---

## 四、参考应用

| 应用 | 特点 | 可借鉴点 |
|------|------|---------|
| **Notion** | 区块编辑、数据库 | 布局设计、模块化 |
| **Obsidian** | Markdown、双向链接 | Markdown 渲染、主题 |
| **Flomo** | 快速记录、标签串联 | 快速输入、分享 |
| **Apple Notes** | 简洁、美观 | 卡片设计、交互 |
| **Logseq** | 大纲模式、大纲即笔记 | 大纲视图 |

---

## 五、总结

Momerandum 作为一个轻量级备忘录应用，核心功能已相对完善。优先推荐进行 **UI 改版** 和 **Markdown 支持**，可在短期内显著提升用户体验。后续可根据使用情况，逐步进行技术架构升级。

---

*文档生成时间：2026-04-03*
