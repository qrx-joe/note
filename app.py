from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import json
import os
import uuid
import msvcrt
import shutil
from datetime import datetime

app = Flask(__name__)

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

def backup_data():
    if os.path.exists(DATA_FILE):
        shutil.copy2(DATA_FILE, BACKUP_FILE)

def load_memos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_memos(memos):
    # 先备份
    backup_data()
    # 获取文件锁 (Windows)
    lock_fd = None
    try:
        lock_fd = open(LOCK_FILE, 'w')
        msvcrt.locking(lock_fd.fileno(), msvcrt.LK_LOCK, 1)
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(memos, f, ensure_ascii=False, indent=2)
        finally:
            msvcrt.locking(lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
    finally:
        if lock_fd:
            lock_fd.close()

@app.route('/')
def index():
    memos = load_memos()

    # 置顶的放最前面
    memos = sorted(memos, key=lambda m: (not m.get('pinned', False), m.get('created_at', '')), reverse=True)

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
    
    if not title or not content:
        flash('标题和内容都不能为空！')
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

        if not title or not content:
            flash('标题和内容都不能为空！')
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

if __name__ == '__main__':
    app.run(debug=True)