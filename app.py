import os
import uuid
import datetime
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 配置資訊
GITHUB_USER = "jimmy0800"
REPO_NAME = "my-html-share"
EXPORT_DIR = "docs"

if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

def sync_to_github(file_name):
    """將變更同步至 GitHub"""
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"發布新網頁: {file_name}"], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except Exception as e:
        print(f"Git 同步失敗: {e}")
        return False

def update_index_html(history):
    """在 docs 資料夾內生成 index.html，作為靜態網頁的首頁"""
    items_html = "".join([f'<li><a href="{i["url"]}">{i["name"]}</a></li>' for i in history])
    index_content = f"""
    <!DOCTYPE html><html><head><meta charset="utf-8">
    <title>我的 HTML 分享清單</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:sans-serif;padding:20px;line-height:1.6;}} li{{margin-bottom:10px;}}</style>
    </head>
    <body><h1>📂 歷史發布列表</h1><ul>{items_html}</ul></body></html>
    """
    with open(os.path.join(EXPORT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_content)

def get_history():
    """掃描 docs 資料夾並產生歷史連結列表"""
    if not os.path.exists(EXPORT_DIR): return []
    # 排除 index.html 自身，只列出 HTML 檔案
    files = sorted([f for f in os.listdir(EXPORT_DIR) if f.endswith(".html") and f != "index.html"], reverse=True)
    history = []
    for f in files:
        url = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/{f}"
        history.append({"name": f, "url": url})
    return history

# --- 介面保持不變 ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>HTML 雲端發布中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; background: #f0f2f5; color: #333; }
        .container { max-width: 700px; margin: auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2, h3 { color: #007bff; }
        textarea { width: 100%; height: 200px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 8px; font-family: monospace; padding: 12px; box-sizing: border-box; }
        input[type="text"] { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 8px; font-size: 1.1rem; cursor: pointer; font-weight: bold; }
        .history-list { margin-top: 30px; border-top: 2px solid #eee; padding-top: 20px; }
        .history-item { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #fafafa; font-size: 14px; }
        .history-item a { color: #007bff; text-decoration: none; }
        .success-box { background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin-bottom: 20px; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 HTML 雲端發布中心</h2>
        {% if final_url %}
        <div class="success-box">
            <strong>✅ 發布成功！</strong> (部署需約 1 分鐘)<br>
            <a href="{{ final_url }}" target="_blank">{{ final_url }}</a>
        </div>
        {% endif %}
        <form method="POST">
            <input type="text" name="custom_name" placeholder="請輸入檔名 (選填)">
            <textarea name="code" placeholder="請在此貼上代碼..." required></textarea>
            <button type="submit">立即發布至 GitHub Pages</button>
        </form>
        <div class="history-list">
            <h3>📂 歷史發布列表</h3>
            {% for item in history %}
            <div class="history-item">
                <span>{{ item.name }}</span>
                <a href="{{ item.url }}" target="_blank">查看頁面</a>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    final_url = None
    if request.method == 'POST':
        code = request.form.get('code', '')
        user_name = request.form.get('custom_name', '').strip()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        
        if user_name:
            file_name = f"{timestamp}_{user_name}.html"
        else:
            file_name = f"{timestamp}_{uuid.uuid4().hex[:4]}.html"
            
        file_path = os.path.join(EXPORT_DIR, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        # 關鍵修正：同時更新靜態索引頁面
        current_history = get_history()
        update_index_html(current_history)
        
        if sync_to_github(file_name):
            final_url = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/{file_name}"
        
    return render_template_string(HTML_UI, final_url=final_url, history=get_history())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)