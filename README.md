# Momentum - 备忘录应用

一个简洁优雅的备忘录应用，基于 Flask 构建，帮助你轻松记录和管理日常灵感与任务。

## 功能特性

- **侧边栏导航** — 左侧笔记列表 + 搜索 + 标签筛选，右侧展示详情
- **标签系统** — 为笔记添加标签，快速分类和筛选
- **全文搜索** — 支持按标题和内容搜索笔记
- **置顶功能** — 重要笔记置顶显示，优先展示
- **数据备份** — 自动备份机制，防止数据丢失
- **文件锁保护** — 并发写入安全，避免数据损坏
- **响应式设计** — 适配桌面端和移动端
- **暖橙主题** — 简约舒适的视觉风格

## 技术栈

- **后端**: Flask 3.1+ + Flask-WTF (CSRF 保护)
- **数据存储**: JSON 文件 + portalocker 文件锁
- **前端**: Jinja2 模板 + 原生 CSS
- **包管理**: uv
- **代码质量**: ruff (lint/format) + mypy (类型检查) + pytest (测试) + bandit (安全扫描)
- **CI/CD**: GitHub Actions

## 项目结构

```
momentum/
├── app.py                  # Flask 应用主文件
├── pyproject.toml          # 项目配置与依赖
├── uv.lock                 # uv 锁定文件
├── memos.json              # 数据存储文件
├── memos.json.bak          # 自动备份文件
├── start.bat               # Windows 一键启动脚本
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions 流水线
├── static/
│   └── style.css           # 样式文件
├── templates/
│   └── index.html          # 单页应用模板
└── tests/
    └── test_app.py         # 单元测试
```

## 快速开始

### 环境要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装与运行

1. **克隆项目**
   ```bash
   git clone <仓库地址>
   cd momentum
   ```

2. **创建虚拟环境**
   ```bash
   uv venv
   ```

3. **安装依赖**
   ```bash
   uv sync
   ```

4. **启动应用**
   ```bash
   uv run app.py
   ```

5. **访问应用**
   打开浏览器访问 `http://localhost:5000`

### Windows 一键启动

双击 `start.bat` 即可自动寻找可用端口（5000-5010）并启动应用。

## 使用指南

### 创建笔记
点击左侧「新建笔记」按钮，填写标题、内容和标签，点击保存。

### 编辑笔记
在笔记详情页点击「编辑」按钮，修改后保存。

### 删除笔记
在笔记详情页点击「删除」按钮，确认后删除。

### 置顶笔记
在笔记详情页点击「置顶」按钮，置顶笔记会显示在列表最上方。

### 搜索与筛选
- 在左侧搜索框输入关键词，按回车搜索
- 点击标签快速筛选同类笔记
- 点击搜索框旁的清除按钮重置筛选

## 开发指南

### 运行测试

```bash
uv run pytest tests/ -v
```

### 代码检查

```bash
# lint 检查
uv run ruff check app.py tests/

# 格式检查
uv run ruff format --check app.py tests/

# 类型检查
uv run mypy app.py

# 安全扫描
uv run bandit -r app.py
```

### 添加依赖

```bash
uv add package-name        # 生产依赖
uv add --dev package-name  # 开发依赖
```

## CI/CD 流水线

每次推送到 `master` 分支会自动触发以下检查：

| 任务 | 工具 | 说明 |
|------|------|------|
| 代码规范 | ruff | lint + format 检查 |
| 类型检查 | mypy | 静态类型分析 |
| 单元测试 | pytest | 测试覆盖率 >= 50% |
| 安全扫描 | bandit | 安全漏洞检测 |

## 数据安全

- **自动备份**: 每次保存数据前自动创建 `memos.json.bak`
- **损坏恢复**: 主数据文件损坏时自动从备份恢复
- **文件锁**: 使用 portalocker 防止并发写入导致数据损坏
- **类型校验**: 保存前校验数据格式，防止非法写入

## 自定义配置

### 修改密钥
删除 `.secret_key` 文件，下次启动会自动生成新密钥。

### 修改数据文件路径
在 `app.py` 中修改：
```python
DATA_FILE = 'custom/path/to/memos.json'
BACKUP_FILE = 'custom/path/to/memos.json.bak'
```

### 修改主题色
在 `static/style.css` 中修改 CSS 变量：
```css
:root {
    --accent: #FF8A65;        /* 主题色 */
    --accent-hover: #FF7A50;  /* 悬停色 */
    --accent-light: #FFF4F0;  /* 浅色背景 */
}
```

## 参与贡献

1. Fork 本项目
2. 创建功能分支：`git checkout -b feature/新功能`
3. 提交更改：`git commit -m '添加新功能'`
4. 推送分支：`git push origin feature/新功能`
5. 创建 Pull Request

## 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。
