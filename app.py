from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
import json
import os
import uuid
import shutil
import portalocker
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 环境变量控制 debug 模式
app.debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

# 安全地生成 secret_key
SECRET_KEY_FILE = '.secret_key'
if os.path.exists(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, 'rb') as f:
        app.secret_key = f.read()
else:
    app.secret_key = os.urandom(32)
    with open(SECRET_KEY_FILE, 'wb') as f:
        f.write(app.secret_key)

# 初始化 CSRF 保护
csrf = CSRFProtect(app)

DATA_FILE = 'memos.json'
BACKUP_FILE = 'memos.json.bak'
LOCK_FILE = 'memos.lock'

# 输入限制常量
MAX_TITLE = 200
MAX_CONTENT = 50000

def backup_data():
    if os.path.exists(DATA_FILE):
        shutil.copy2(DATA_FILE, BACKUP_FILE)

def load_memos():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"数据文件损坏: {e}")
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info("已从备份文件恢复数据")
                return data
            except (json.JSONDecodeError, IOError) as be:
                logger.error(f"备份文件也损坏: {be}")
        raise RuntimeError(
            "数据文件和备份文件均已损坏，无法恢复数据。"
            "请手动检查 memos.json 和 memos.json.bak"
        )

def save_memos(memos):
    if not isinstance(memos, list):
        raise TypeError("memos 必须是列表类型")
    backup_data()
    try:
        with portalocker.Lock(LOCK_FILE, 'w', timeout=5) as lock_fd:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(memos, f, ensure_ascii=False, indent=2)
    except portalocker.LockException as e:
        logger.error(f"保存文件失败: {e}")
        raise

@app.route('/')
def validate_memo_input(title, content):
    if not title or not content:
        return '标题和内容都不能为空！'
    if len(title) > MAX_TITLE:
        return f'标题不能超过{MAX_TITLE}字符！'
    if len(content) > MAX_CONTENT:
        return f'内容不能超过{MAX_CONTENT}字符！'
    return None

def index():
    memos = load_memos()

    # 置顶的放最前面，同类型按时间倒序（新的在前）
    memos = sorted(memos, key=lambda m: m.get('created_at', ''), reverse=True)
    memos = sorted(memos, key=lambda m: not m.get('pinned', False))

    # 搜索
    q = request.args.get('q', '').strip()
    if q:
        q_lower = q.lower()
        memos = [m for m in memos if q_lower in m.get('title', '').lower() or q_lower in m.get('content', '').lower()]

    # 按标签筛选
    tag = request.args.get('tag', '').strip()
    if tag:
        memos = [m for m in memos if tag in m.get('tags', [])]

    # 分页
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(memos)
    memos_page = memos[(page-1)*per_page:page*per_page]
    has_prev = page > 1
    has_next = page * per_page < total

    # 获取所有标签
    all_tags = set()
    for m in memos:
        all_tags.update(m.get('tags', []))
    all_tags = sorted(all_tags)

    return render_template('index.html', memos=memos_page, search_query=q, page=page, has_prev=has_prev, has_next=has_next, current_tag=tag, all_tags=all_tags)

@app.route('/add', methods=['POST'])
def add_memo():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    error = validate_memo_input(title, content)
    if error:
        flash(error)
        return redirect(url_for('index'))

    tags_raw = request.form.get('tags', '').strip()
    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

    memos = load_memos()
    new_memo = {
        'id': str(uuid.uuid4()),
        'title': title,
        'content': content,
        'tags': tags,
        'pinned': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    memos.insert(0, new_memo)
    save_memos(memos)
    flash('备忘录添加成功！')
    return redirect(url_for('index'))

@app.route('/edit/<memo_id>', methods=['GET', 'POST'])
def edit_memo(memo_id):
    memos = load_memos()
    memo = next((m for m in memos if m['id'] == memo_id), None)
    
    if not memo:
        flash('备忘录不存在！')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags_raw = request.form.get('tags', '').strip()
        tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

        error = validate_memo_input(title, content)
        if error:
            flash(error)
            return redirect(url_for('edit_memo', memo_id=memo_id))

        memo['title'] = title
        memo['content'] = content
        memo['tags'] = tags
        memo['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        save_memos(memos)
        flash('备忘录更新成功！')
        return redirect(url_for('index'))
    
    return render_template('edit.html', memo=memo)

@app.route('/delete/<memo_id>', methods=['POST'])
def delete_memo(memo_id):
    memos = load_memos()
    memos = [m for m in memos if m['id'] != memo_id]
    save_memos(memos)
    flash('备忘录删除成功！')
    return redirect(url_for('index'))

@app.route('/pin/<memo_id>', methods=['POST'])
def pin_memo(memo_id):
    memos = load_memos()
    memo = next((m for m in memos if m['id'] == memo_id), None)
    if memo:
        memo['pinned'] = not memo.get('pinned', False)
        save_memos(memos)
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """健康检查端点"""
    # 检查数据文件
    data_ok = os.path.exists(DATA_FILE)
    backup_ok = os.path.exists(BACKUP_FILE)

    status = 'healthy' if data_ok else 'degraded'
    return jsonify({
        'status': status,
        'data_file': data_ok,
        'backup_file': backup_ok
    }), 200 if data_ok else 503

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"启动应用: debug={debug}, port={port}")
    app.run(host='127.0.0.1', port=port, debug=debug)