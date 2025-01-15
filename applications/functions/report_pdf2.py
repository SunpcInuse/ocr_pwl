import base64
import cv2
import json
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from applications.functions.task import OCRWebUtils

# 注册字体
pdfmetrics.registerFont(TTFont('SimHei', 'applications/functions/lib/SimHei.ttf'))  # 注册字体,字体类

# 初始化OCR工具
ocr_utils = OCRWebUtils()  # 需要修改为rapidocr调用


class RLPDF2:
    def __init__(self, output_pdf_path, dpi=72, alpha=0):
        self.output_pdf_path = output_pdf_path  # 输出PDF文件路径
        self.dpi = dpi  # 图像的DPI，默认为72
        self.alpha = alpha

    def read_local_image(self, file_path: str) -> str:
        """
        读取本地图片并返回Base64编码。
        """
        img = cv2.imread(file_path)
        if img is None:
            raise FileNotFoundError(f"Image not found at path: {file_path}")

        # 将图片编码为Base64字符串
        _, img_encoded = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        return img_base64

    def perform_ocr(self, file_path):
        """
        使用OCR识别并返回文本和位置信息。
        """
        rec_det_list = []
        img_base64 = self.read_local_image(file_path)
        ocr_result = ocr_utils("data:image/jpeg;base64," + img_base64)

        if isinstance(ocr_result, str):
            ocr_result = json.loads(ocr_result)

        rec_res = ocr_result.get("rec_res")
        det_boxes = ocr_result.get("det_boxes")

        if isinstance(rec_res, str):
            rec_res = json.loads(rec_res)

        if len(rec_res) != len(det_boxes):
            raise ValueError("识别错误,检测与识别列表长度不一致")

        for rec, det in zip(rec_res, det_boxes):
            rec_det_list.append([det, rec[1]])

        return rec_det_list

    def calculate_font_size_for_textblock(self, bbox, text):
        """
        根据文本框的高度和宽度推算字体大小。
        """
        text_width = bbox[1][0] - bbox[0][0]  # 文本框的宽度
        text_height = bbox[2][1] - bbox[0][1]  # 文本框的高度

        font_size_based_on_height = text_height  # 假设字体的高度与文本框高度一致

        # 平均字符宽度，假设字符宽度为文本框宽度除以字符数
        avg_char_width = text_width / len(text) if len(text) > 0 else text_width  # 每个字符的平均宽度
        font_size_based_on_width = text_width * 0.9 / (len(text) * avg_char_width) * font_size_based_on_height

        font_size = min(font_size_based_on_height, font_size_based_on_width)
        return font_size

    def adjust_y_position(self, img_height, ocr_y, font_size, baseline_offset=0):
        """
        调整y坐标，确保文字在PDF中的正确位置。
        """
        pdf_y = img_height - ocr_y  # PDF坐标系是从下到上
        adjusted_y = pdf_y - font_size + baseline_offset  # 调整 y 位置，避免文字偏高
        return adjusted_y

    def add_ocr_text_to_pdf(self, image_path, ocr_result, c):
        """
        在PDF中添加OCR识别的文本层，位置和文本对应
        """
        img = Image.open(image_path)
        img_width, img_height = img.size

        # 插入图像作为底层
        c.drawImage(image_path, 0, 0, width=img_width, height=img_height)

        # 处理OCR结果并将文本添加到PDF中
        for block in ocr_result:
            bbox = block[0]  # 文本框的四个角坐标
            text = block[1]  # OCR识别的文本

            # 计算文本框的左上角坐标，使用第一个坐标
            x, y = bbox[0][0], bbox[0][1]
            font_size = self.calculate_font_size_for_textblock(bbox, text)
            adjusted_y = self.adjust_y_position(img_height, y, int(font_size))

            # 设置字体和颜色
            c.setFont('SimHei', font_size)  # 使用SimHei字体
            c.setFillColorRGB(0, 0, 0, alpha=self.alpha)  # 设置透明度为0，完全透明

            # 绘制文字到PDF上
            c.drawString(x, adjusted_y, text)

    def create_pdf_from_images(self, image_paths):
        """
        创建一个PDF文件，支持多个图像文件输入。
        """
        # 初始化canvas，输出的PDF将具有与每个图像相同的大小
        c = canvas.Canvas(r"D:\Project\OCR-demo\downloads/{}.pdf".format(self.output_pdf_path))

        for image_path in image_paths:
            # 进行OCR识别
            ocr_result = self.perform_ocr(image_path)

            # 获取图像的宽度和高度
            img = Image.open(image_path)
            img_width, img_height = img.size

            # 根据图像大小创建PDF页面
            c.setPageSize((img_width, img_height))

            # 创建PDF并插入图像
            self.create_pdf_with_image(image_path, c)

            # 在PDF上添加OCR文本
            self.add_ocr_text_to_pdf(image_path, ocr_result, c)

            # 添加一个新的页面
            c.showPage()

        # 保存PDF
        c.save()

    def create_pdf_with_image(self, image_path, c):
        """
        在PDF中添加图像，作为第一层
        """
        img = Image.open(image_path)
        img_width, img_height = img.size

        # 插入图像作为底层
        c.drawImage(image_path, 0, 0, width=img_width, height=img_height)

# 示例使用
# image_paths = ["test.png", "test.jpg"]  # 图像文件路径列表
# output_pdf_path = "output.pdf"  # 输出PDF文件路径

# 创建OCRToPDF对象并生成PDF
# ocr_to_pdf = RLPDF2(output_pdf_path)
# ocr_to_pdf.create_pdf_from_images(image_paths)
