# Lumi Notes PRD 评审意见与补充方案

> 评审时间：2026-04-04 | 版本：V1.0 | 评审人：Claude | 状态：待补充

---

## 一、总体评价

### 1.1 文档质量

| 维度 | 评分 | 说明 |
|------|------|------|
| 结构完整性 | 8/10 | 具备核心章节，但缺少技术实现细节 |
| 功能描述 | 7/10 | 需求清晰但AI功能过于笼统 |
| 可开发性 | 5/10 | 缺少技术选型和API设计，无法直接开工 |
| 安全性 | 6/10 | 提及JWT但细节不足 |

### 1.2 结论

**当前状态：需要补充**

该PRD可作为产品需求确认文档，但必须补充以下章节后方可进入开发阶段：
1. 技术选型章节
2. 完整API接口设计
3. AI服务集成方案
4. 安全加固细节
5. 数据模型细化

---

## 二、缺失内容清单

| 类别 | 缺失项 | 优先级 | 影响 |
|------|--------|--------|------|
| 技术选型 | 前端/后端/数据库/AI服务 | P0 | 开发团队无法确定技术方向 |
| API设计 | 接口文档、请求响应格式 | P0 | 前后端无法对接 |
| AI方案 | 模型选择、成本、超时处理 | P1 | 功能无法落地 |
| 安全细节 | JWT刷新、XSS、CSRF | P1 | 生产环境风险 |
| 数据模型 | 字段约束、索引设计 | P1 | 数据库无法设计 |

---

## 三、技术选型建议

### 3.1 推荐技术栈

```
┌─────────────────────────────────────────────────────────┐
│                      技术架构总览                         │
├─────────────────────────────────────────────────────────┤
│  前端 Web    │ Vue 3 + TypeScript + TailwindCSS         │
│  前端 Mobile │ UniApp (Vue语法，一套代码双端)            │
│  后端        │ Node.js + NestJS                        │
│  数据库      │ PostgreSQL (主) + Redis (缓存)           │
│  AI服务      │ OpenAI API (GPT-3.5-turbo)              │
│  部署        │ Docker + CI/CD                           │
└─────────────────────────────────────────────────────────┘
```

### 3.2 选型理由

| 组件 | 推荐方案 | 理由 |
|------|----------|------|
| 前端框架 | Vue 3 | 响应式、组件化、文档完善，与"极简高效"理念契合 |
| CSS框架 | TailwindCSS | 原子化CSS，易实现莫兰迪色系定制 |
| 移动端 | UniApp | Vue语法，一套代码同时输出iOS/Android/Web |
| 后端框架 | NestJS | TypeScript原生、模块化、装饰器语法优雅 |
| 数据库 | PostgreSQL | 复杂查询支持、JSON支持、ACID可靠 |
| 缓存 | Redis | 搜索结果缓存、会话存储 |
| AI | OpenAI GPT-3.5-turbo | 成本可控(~$0.002/1k tokens)、效果足够 |

### 3.3 第三方服务

| 服务 | 用途 | 预估成本 |
|------|------|----------|
| Vercel/Netlify | 前端托管 | 免费版足够 |
| Railway/Render | 后端部署 | $5/月起 |
| Supabase | PostgreSQL + Auth | 免费版足够 |
| OpenAI | AI功能 | ~$10/月（初期） |

---

## 四、API接口设计

### 4.1 接口规范

- 协议：RESTful
- 认证：Bearer Token (JWT)
- 数据格式：`Content-Type: application/json`
- 错误码规范：

```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

### 4.2 认证接口 (Auth)

#### 4.2.1 注册

```
POST /api/auth/register
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "min8chars",
  "nickname": "Lumi"
}
```

**Response (200):**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "nickname": "Lumi",
      "avatar": null
    },
    "accessToken": "eyJhbG...",
    "refreshToken": "eyJhbG..."
  }
}
```

#### 4.2.2 登录

```
POST /api/auth/login
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "min8chars"
}
```

**Response (200):** 同注册

#### 4.2.3 刷新令牌

```
POST /api/auth/refresh
```

**Request:**
```json
{
  "refreshToken": "eyJhbG..."
}
```

**Response (200):**
```json
{
  "code": 200,
  "data": {
    "accessToken": "new_access_token",
    "refreshToken": "new_refresh_token"
  }
}
```

#### 4.2.4 获取/更新个人资料

```
GET /api/auth/profile
PUT /api/auth/profile
```

**PUT Request:**
```json
{
  "nickname": "NewNickname",
  "avatar": "base64或URL"
}
```

### 4.3 笔记接口 (Notes)

#### 4.3.1 获取笔记列表

```
GET /api/notes?page=1&limit=20&tagId=xxx&archived=false
```

**Response (200):**
```json
{
  "code": 200,
  "data": {
    "list": [
      {
        "id": "uuid",
        "title": "笔记标题",
        "summary": "AI生成的摘要...",
        "tags": ["Tech", "Idea"],
        "isPinned": true,
        "isArchived": false,
        "updatedAt": "2026-04-04T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "hasMore": true
    }
  }
}
```

#### 4.3.2 获取单条笔记

```
GET /api/notes/:id
```

**Response (200):**
```json
{
  "code": 200,
  "data": {
    "id": "uuid",
    "title": "笔记标题",
    "content": "# Markdown内容...",
    "tags": ["Tech"],
    "isPinned": false,
    "isArchived": false,
    "createdAt": "2026-04-01T10:00:00Z",
    "updatedAt": "2026-04-04T12:00:00Z"
  }
}
```

#### 4.3.3 创建笔记

```
POST /api/notes
```

**Request:**
```json
{
  "title": "笔记标题",
  "content": "# Markdown内容...",
  "tags": ["Tech", "Idea"]
}
```

#### 4.3.4 更新笔记

```
PUT /api/notes/:id
```

**Request:** 同创建，可部分更新

#### 4.3.5 删除笔记

```
DELETE /api/notes/:id
```

**逻辑删除：** 将 `isDeleted` 标记为 true，放入回收站

#### 4.3.6 彻底删除

```
DELETE /api/notes/:id/permanent
```

#### 4.3.7 置顶/取消置顶

```
POST /api/notes/:id/pin
```

**Request:**
```json
{
  "pinned": true
}
```

#### 4.3.8 归档/取消归档

```
POST /api/notes/:id/archive
```

**Request:**
```json
{
  "archived": true
}
```

#### 4.3.9 搜索笔记

```
GET /api/notes/search?q=关键词&page=1&limit=20
```

**Response:** 同列表接口，关键词高亮在客户端处理

#### 4.3.10 自动保存草稿

```
POST /api/notes/:id/draft
```

**Request:**
```json
{
  "title": "标题",
  "content": "内容..."
}
```

**说明：** 停止输入2秒后前端自动调用，保存到 `draft` 字段

### 4.4 标签接口 (Tags)

#### 4.4.1 获取标签列表

```
GET /api/tags
```

**Response (200):**
```json
{
  "code": 200,
  "data": [
    { "id": "uuid", "name": "Tech", "color": "#7C3AED" },
    { "id": "uuid", "name": "Idea", "color": "#10B981" }
  ]
}
```

#### 4.4.2 获取某标签下的笔记

```
GET /api/tags/:id/notes?page=1&limit=20
```

### 4.5 AI接口 (AI)

#### 4.5.1 生成摘要

```
POST /api/ai/summarize
```

**Request:**
```json
{
  "content": "长篇Markdown内容..."
}
```

**Response (200):**
```json
{
  "code": 200,
  "data": {
    "summary": "20字以内的摘要"
  }
}
```

**触发条件：** 笔记内容 > 500 字

#### 4.5.2 推荐标签

```
POST /api/ai/suggest-tags
```

**Request:**
```json
{
  "title": "笔记标题",
  "content": "笔记内容..."
}
```

**Response (200):**
```json
{
  "code": 200,
  "data": {
    "tags": ["Tech", "编程", "学习"]
  }
}
```

**说明：** 返回1-3个标签，用户可选择采纳

---

## 五、数据模型细化

### 5.1 用户表 (users)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nickname VARCHAR(50) DEFAULT '新用户',
  avatar VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### 5.2 笔记表 (notes)

```sql
CREATE TABLE notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(100) NOT NULL,
  content TEXT,
  summary VARCHAR(100),  -- AI生成的摘要
  draft TEXT,  -- 自动保存的草稿
  is_pinned BOOLEAN DEFAULT false,
  is_archived BOOLEAN DEFAULT false,
  is_deleted BOOLEAN DEFAULT false,  -- 软删除
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_user_pinned ON notes(user_id, is_pinned DESC, updated_at DESC);
CREATE INDEX idx_notes_user_archived ON notes(user_id, is_archived, updated_at DESC);
CREATE INDEX idx_notes_title_search ON notes USING gin(to_tsvector('simple', title || ' ' || COALESCE(content, '')));
```

### 5.3 标签表 (tags)

```sql
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(50) NOT NULL,
  color VARCHAR(20) DEFAULT '#6B7280',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_tags_user_name ON tags(user_id, name);
```

### 5.4 笔记-标签关联表 (note_tags)

```sql
CREATE TABLE note_tags (
  note_id UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
  tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (note_id, tag_id)
);

CREATE INDEX idx_note_tags_note ON note_tags(note_id);
CREATE INDEX idx_note_tags_tag ON note_tags(tag_id);
```

### 5.5 令牌表 (tokens)

```sql
CREATE TABLE tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  refresh_token VARCHAR(500) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tokens_user ON tokens(user_id);
```

---

## 六、AI集成方案

### 6.1 模型选择

| 功能 | 推荐模型 | 理由 |
|------|----------|------|
| 摘要生成 | GPT-3.5-turbo | 成本低，效果足够 |
| 标签推荐 | GPT-3.5-turbo | 理解力强 |

### 6.2 调用流程

```
用户创建/编辑笔记
       │
       ▼
内容长度判断 (>500字?)
       │
   ┌───┴───┐
   │       │
  是      否
   │       │
   ▼       ▼
调用 /ai/summarize    跳过
   │       
   ▼       
存储摘要到 summary 字段
```

### 6.3 超时处理

| 场景 | 处理方式 |
|------|----------|
| AI响应 > 5秒 | 返回前端"摘要生成中"，后台继续处理 |
| AI调用失败 | 记录日志，摘要字段为空，不阻塞用户 |
| 免费额度用完 | 提示用户，关闭AI功能入口 |

### 6.4 成本控制

- 每月AI预算：$20
- 单次摘要调用预估：~1000 tokens = $0.002
- 每月可调用：~10000次（足够初期使用）

### 6.5 隐私说明

- 用户可随时在设置中关闭AI功能
- AI调用日志仅保存错误记录，不保存内容
- 用户数据不会用于模型训练

---

## 七、安全加固方案

### 7.1 认证机制

```
Access Token:
  有效期：15分钟
  存储：Memory (内存)
  用途：API请求认证

Refresh Token:
  有效期：7天
  存储：HttpOnly Cookie (防XSS)
  用途：续期Access Token
```

### 7.2 密码安全

- 存储：Bcrypt hash (cost factor = 12)
- 传输：HTTPS only
- 限制：密码最小8位

### 7.3 输入过滤

| 场景 | 方案 |
|------|------|
| Markdown渲染 | DOMPurify (前端) + dompurify (后端) |
| XSS防护 | Content Security Policy |
| SQL注入 | Parameterized Queries (ORM) |

### 7.4 速率限制

| 接口 | 限制 |
|------|------|
| 登录/注册 | 10次/分钟 |
| 笔记操作 | 60次/分钟 |
| AI接口 | 20次/分钟 |

### 7.5 CORS配置

```javascript
// 允许的来源
const ALLOWED_ORIGINS = [
  'http://localhost:3000',
  'https://luminotes.app',
  'https://www.luminotes.app'
];
```

---

## 八、非功能性需求细化

### 8.1 响应式设计

| 断点 | 宽度 | 布局 |
|------|------|------|
| Mobile | < 640px | 单列，卡片式 |
| Tablet | 640px - 1024px | 侧边栏折叠 |
| Desktop | > 1024px | 完整侧边栏 + 网格 |

### 8.2 性能指标

| 指标 | 目标值 |
|------|--------|
| 首屏加载 | < 1.5s |
| 搜索响应 | < 200ms |
| 笔记列表分页 | 20条/页 |
| AI摘要生成 | < 3s |

### 8.3 兼容性

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- iOS >= 14
- Android >= 10

### 8.4 无网络处理

| 场景 | 处理 |
|------|------|
| 创建/编辑笔记 | 提示"网络不可用，内容已本地保存" |
| 刷新页面 | 提示"网络不可用，无法获取最新数据" |
| 操作完成 | Toast提示："操作成功（同步中）" |

---

## 九、项目里程碑

### Phase 1: 基础功能 (2周)

- [ ] 用户注册/登录
- [ ] 笔记CRUD
- [ ] 标签管理
- [ ] 基础搜索

### Phase 2: AI功能 (1周)

- [ ] 摘要自动生成
- [ ] 标签智能推荐
- [ ] 错误处理与回退

### Phase 3: 优化 (1周)

- [ ] 性能优化（缓存、索引）
- [ ] 移动端适配
- [ ] 安全加固
- [ ] 测试与Bug修复

---

## 十、结论

该PRD作为V1.0版本的产品需求文档框架完整，但技术实现细节缺失。

**必须补充内容：**
1. 技术选型确认（本文提供建议方案）
2. 完整API接口设计（本文已提供）
3. AI服务集成方案（本文已提供）
4. 安全加固细节（本文已提供）

**下一步行动：**
- 产品确认技术选型
- 后端设计数据库表结构
- 前后端开始API对接
- AI服务接入测试

---

> 评审完成时间：2026-04-04
> 文档版本：1.1