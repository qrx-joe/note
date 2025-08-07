from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DATA_FILE = 'memos.json'

def load_memos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_memos(memos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    memos = load_memos()
    return render_template('index.html', memos=memos)

@app.route('/add', methods=['POST'])
def add_memo():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title or not content:
        flash('标题和内容都不能为空！')
        return redirect(url_for('index'))
    
    memos = load_memos()
    new_memo = {
        'id': len(memos) + 1,
        'title': title,
        'content': content,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    memos.insert(0, new_memo)
    save_memos(memos)
    flash('备忘录添加成功！')
    return redirect(url_for('index'))

@app.route('/edit/<int:memo_id>', methods=['GET', 'POST'])
def edit_memo(memo_id):
    memos = load_memos()
    memo = next((m for m in memos if m['id'] == memo_id), None)
    
    if not memo:
        flash('备忘录不存在！')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('标题和内容都不能为空！')
            return redirect(url_for('edit_memo', memo_id=memo_id))
        
        memo['title'] = title
        memo['content'] = content
        memo['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        save_memos(memos)
        flash('备忘录更新成功！')
        return redirect(url_for('index'))
    
    return render_template('edit.html', memo=memo)

@app.route('/delete/<int:memo_id>')
def delete_memo(memo_id):
    memos = load_memos()
    memos = [m for m in memos if m['id'] != memo_id]
    save_memos(memos)
    flash('备忘录删除成功！')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)