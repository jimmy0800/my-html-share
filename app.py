import os
import uuid
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 配置：檔案會存放在 docs 資料夾（GitHub Pages 常用的路徑）
EXPORT_DIR = "docs"
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

# --- 自動推送到 GitHub 的函式 ---
def sync_to_github(file_name):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Add new HTML: {file_name}"], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except Exception as e:
        print(f"Git Push 失敗: {e}")
        return False

# --- 輸入介面 ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Codespaces 雲端發布</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f4f4f4; }
        .box { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
        textarea { width: 100%; height: 300px; margin-bottom: 10px; border: 1px solid #ccc; padding: 10px; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
    </style>
</head>
<body>
    <div class="box">
        <h3>貼上 HTML 並發布至 Pages</h3>
        <form method="POST">
            <textarea name="code" placeholder="請在此貼上 HTML..." required></textarea>
            <button type="submit">發布至靜態網頁</button>
        </form>
        {% if final_url %}
        <div style="margin-top:20px; padding:15px; background:#d4edda; border-radius:5px;">
            <strong>✅ 發布成功！</strong><br>
            靜態預覽網址 (需等約 1 分鐘部署)：<br>
            <a href="{{ final_url }}" target="_blank">{{ final_url }}</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    final_url = None
    if request.method == 'POST':
        code = request.form.get('code', '')
        file_id = str(uuid.uuid4())[:8]
        file_name = f"{file_id}.html"
        file_path = os.path.join(EXPORT_DIR, file_name)
        
        # 1. 存入檔案
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        # 2. 自動同步到 GitHub
        if sync_to_github(file_name):
            # 這裡換成你的 GitHub Pages 網址格式
            # 格式通常是: https://帳號名.github.io/專案名/檔案名
            username = "你的GitHub帳號"
            repo_name = "my-html-share"
            final_url = f"https://{username}.github.io/{repo_name}/{file_name}"
        
    return render_template_string(HTML_UI, final_url=final_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)