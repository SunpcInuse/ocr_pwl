from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os, cv2, base64, json, re
from applications import app
from . import demo_bp
from datetime import datetime
from applications.functions.layout_word import LayoutWord


@demo_bp.route('/layout', methods=['GET'])
def url_ocr_layout():
    if request.method == "GET":
        return render_template("layout_demo.html")

@demo_bp.route('/upload_layout', methods=['POST'])
def layout_pic_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')  # 获取上传的文件列表
    filenamePrefix = request.form.get('filenamePrefix', '')  # 捕获文件名称标识
    time2date_folder = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], time2date_folder), exist_ok=True)
    save_path_list = []
    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # 保存文件
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], time2date_folder + '/' + filename)
        file.save(save_path)
        save_path_list.append(save_path)
    print(save_path_list)
    lw = LayoutWord(filenamePrefix)
    lw.generate_word_document(save_path_list)
    return jsonify({'message': 'Files successfully uploaded'}), 200

@demo_bp.route('/download_layout', methods=['GET'])
def download_layout():
    # 指定PDF文件的路径
    if request.method == "GET":
        # print(request)
        # print(filename)
        filename = request.args.get('filename')
        docx_path = r'D:\Project\OCR-demo\downloads/{}.docx'.format(filename)
        # 使用send_file发送WORD文件
        return send_file(docx_path, as_attachment=True)


def sort_file_name(test_list):
    _, file_extension = os.path.splitext(test_list[0])
    test_list = [filename.replace(file_extension, "") for filename in test_list]
    print(test_list)
    min_length = find_prefix(test_list)
    # 如果遍历完所有字符都相同，则返回最短字符串的长度
    test_list.sort(key=natural_sort_key)
    test_list = [filename + file_extension for filename in test_list]
    return test_list


def find_prefix(test_list):
    if not test_list:
        return 0

        # 首先找到最短的字符串，因为公共前缀不可能比最短的字符串长
    min_length = min(len(s) for s in test_list)

    # 遍历字符串中的每个字符
    for i in range(min_length):
        # 获取第一个字符串在当前位置的字符
        char = test_list[0][i]
        # 检查其他字符串在相同位置的字符是否相同
        for string in test_list[1:]:
            if string[i] != char:
                return i  # 如果发现不同，则返回当前索引


def natural_sort_key(s):
    # 将字符串分割成数字和非数字部分
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]
