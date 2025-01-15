from flask import Flask
import os
from pathlib import Path
from applications.config import BaseConfig

# 创建主应用
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
app = Flask(__name__, template_folder=ROOT / '../' / BaseConfig.TEMPLATES,
            static_folder=ROOT / '../' / BaseConfig.STATIC)
app.config['UPLOAD_FOLDER'] = 'uploads'  # 设置上传文件夹
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff'}
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 限制文件大小为64MB

from applications.views import demo_bp

app.register_blueprint(demo_bp)
