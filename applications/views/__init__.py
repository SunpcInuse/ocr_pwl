from flask import Blueprint

demo_bp = Blueprint('demo', __name__, url_prefix='/demo')
from applications.views import ocr_demo
from applications.views import ocr_pdf
from applications.views import ocr_layout