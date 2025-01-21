from flask import render_template, request
from . import demo_bp
from applications.functions.task import OCRWebUtils
processor = OCRWebUtils()

@demo_bp.route('/ocr', methods=['GET', 'POST'])
def url_ocr_demo():
    if request.method == "GET":
        return render_template("ocr_demo.html")

    elif request.method == "POST":
        img_str = request.get_json().get("file", None)
        ocr_res = processor(img_str)
        return ocr_res

