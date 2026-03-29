from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import markdown
import os
from datetime import datetime
import json
import sys

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- 新增：静态文件服务 ----------
# 判断是否被打包成 exe
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# 静态文件夹路径（存放 Vue 构建产物）
static_folder = os.path.join(base_path, 'static')
# 确保 static 目录存在（打包后会自动解压到 _MEIPASS/static）
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

# 设置 Flask 静态文件夹
app.static_folder = static_folder
app.static_url_path = ''

# 根路由：返回 index.html（支持 Vue Router history 模式）
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # 如果请求的是静态文件（如 .js, .css），直接返回
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # 否则返回 index.html（前端路由）
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception:
        return "index.html not found. Please check static folder.", 404

@app.route('/api/render', methods=['POST'])
def render_markdown():
    """将 Markdown 渲染为 HTML"""
    data = request.get_json()
    markdown_text = data.get('markdown', '')

    # 使用 markdown 库渲染
    html = markdown.markdown(
        markdown_text,
        extensions=['extra', 'codehilite', 'toc', 'fenced_code']
    )

    return jsonify({'html': html})

@app.route('/api/save', methods=['POST'])
def save_file():
    """保存 Markdown 文件"""
    data = request.get_json()
    content = data.get('content', '')
    filename = data.get('filename', f'document_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')

    # 确保文件名以 .md 结尾
    if not filename.endswith('.md'):
        filename += '.md'

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({
            'success': True,
            'message': '文件保存成功',
            'filepath': filepath,
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'保存失败：{str(e)}'
        }), 500

@app.route('/api/export/html', methods=['POST'])
def export_html():
    """导出为 HTML 文件"""
    data = request.get_json()
    markdown_content = data.get('content', '')
    title = data.get('title', '导出的文档')

    # 渲染 Markdown 为 HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['extra', 'codehilite', 'toc', 'fenced_code']
    )

    # 创建完整的 HTML 文档
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        code {{
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }}
        pre {{
            background-color: #f6f8fa;
            padding: 16px;
            overflow: auto;
            border-radius: 6px;
        }}
        blockquote {{
            border-left: 4px solid #dfe2e5;
            padding-left: 16px;
            color: #6a737d;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #dfe2e5;
            padding: 6px 13px;
        }}
        tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}
        img {{
            max-width: 100%;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

    filename = f'export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_html)

        return jsonify({
            'success': True,
            'message': 'HTML 导出成功',
            'filepath': filepath,
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'导出失败：{str(e)}'
        }), 500

@app.route('/api/files/<filename>', methods=['GET'])
def get_file(filename):
    """获取保存的文件"""
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({'error': '文件不存在'}), 404

@app.route('/api/files', methods=['GET'])
def list_files():
    """列出所有保存的文件"""
    try:
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.md')]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
