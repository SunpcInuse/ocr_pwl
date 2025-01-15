import os

import cv2

from rapid_layout import RapidLayout, VisLayout
from rapidocr_onnxruntime import RapidOCR
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
from rapid_table import RapidTable, VisTable
from rapidocr_onnxruntime import RapidOCR
table_engine = RapidTable()
ocr_engine = RapidOCR()
from seg_table import TABLE2DOC

class LayoutWord():
    def __init__(self, conf_threshold=0.7):
        self.layout_engine = RapidLayout(model_type="pp_layout_cdla", conf_thres=conf_threshold)
        self.engine = RapidOCR()
        self.general_category_list = ['title', 'text', 'figure', 'figure_caption', 'table', 'table_caption', 'header', 'footer',
                                      'reference', 'equation']
        # self.conf_threshold = conf_threshold
        self.vis_save_path = ""

    def layout_pic(self, image_path):
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path
        boxes, scores, class_names, elapse = self.layout_engine(image)
        ploted_img = VisLayout.draw_detections(image, boxes, scores, class_names)
        if ploted_img is not None:  # 将版面分析的结果可视化
            cv2.imwrite("{}layout_res.png".format(self.vis_save_path), ploted_img)
        detection_results = []
        for box, score, class_name in zip(boxes, scores, class_names):
            x1, y1, x2, y2 = box  # x1: 左上角x坐标, y1: 左上角y坐标, x2: 右下角x坐标, y2: 右下角y坐标
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cropped_image = image[y1: y2, x1: x2]
            content = self.extract_text(cropped_image)
            detection_results.append([class_name, content, [x1, y1, x2, y2]])
        print(detection_results)
        detection_results.sort(key=lambda x: x[2][1])
        return image, detection_results

    def extract_text(self, cropped_image):
        result, _ = self.engine(cropped_image)
        content = ""
        for _res in result:
            content += _res[1]  # 正确拼接字符串
        return content

    def header_footer_extract(self, image, detection_results):
        cropped_images = []
        header_content = ""
        footer_content = ""

        for detection in detection_results:
            box, score, class_name = detection[0], detection[1], detection[2]
            # print(box, score, class_name)
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cropped_image = image[y1: y2, x1: x2]
            cropped_images.append(cropped_image)

            if class_name == "header":
                header_content = self.extract_text(cropped_image)
            elif class_name == "footer":
                footer_content = self.extract_text(cropped_image)

        return header_content, footer_content

    def figure_table_extract(self, image):
        pass

    def reference_equation_extract(self, image):
        pass

    def layout_crop_detection(self, image, detection_results):
        cropped_images = []
        header_content = ""
        footer_content = ""

        for detection in detection_results:
            box, score, class_name = detection[0], detection[1], detection[2]
            # print(box, score, class_name)
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cropped_image = image[y1: y2, x1: x2]
            cropped_images.append(cropped_image)

            if class_name == "header":
                header_content = self.extract_text(cropped_image)
            elif class_name == "footer":
                footer_content = self.extract_text(cropped_image)

        print(header_content, footer_content)

    def determine_title_level(self, title):
        if not title:
            return 0
        level = title.strip().count('.') + 1
        return level

    def generate_word_document(self, image_path, output_path):
        # 调用 layout_pic 获取图像和检测结果
        image, total_detection = self.layout_pic(image_path)

        # 创建一个新的 Word 文档
        doc = Document()

        # 遍历检测结果
        for detection in total_detection:
            class_name, content, box = detection

            if class_name == 'text':
                # 添加文本
                doc.add_paragraph(content)
            elif class_name == 'title':
                # 添加标题
                level = self.determine_title_level(content)
                if level > 0:
                    doc.add_heading(content, level=level)
                else:
                    doc.add_heading(content, level=5)
            elif class_name == 'figure':
                # 添加图像
                x1, y1, x2, y2 = box
                cropped_image = image[y1:y2, x1:x2]
                cv2.imwrite("temp_figure.png", cropped_image)
                doc.add_picture("temp_figure.png", width=Inches(4))
            elif class_name == 'figure_caption':
                # 添加图像标题
                doc.add_paragraph(content, style='Caption')
            elif class_name == 'table':
                # 添加表格
                x1, y1, x2, y2 = box
                cropped_image = image[y1:y2, x1:x2]
                cv2.imwrite("temp_table.png", cropped_image)
                ocr_result, _ = ocr_engine("temp_table.png")
                table_html_str, table_cell_bboxes, _ = table_engine("temp_table.png", ocr_result)
                print(table_html_str)
                tbl_engine = TABLE2DOC(doc, table_html_str)
                tbl_engine.main_generate_table(table_html_str)
            elif class_name == 'table_caption':
                # 添加表格标题
                doc.add_paragraph(content, style='Caption')
            elif class_name == 'header':
                # 添加页眉
                section = doc.sections[0]
                header = section.header
                header_paragraph = header.paragraphs[0]
                header_paragraph.text = content
            elif class_name == 'footer':
                # 添加页脚
                section = doc.sections[0]
                footer = section.footer
                footer_paragraph = footer.paragraphs[0]
                footer_paragraph.text = content
            elif class_name == 'reference':
                # 添加参考文献
                doc.add_paragraph(content, style='ListNumber')
            elif class_name == 'equation':
                # 添加公式
                doc.add_paragraph(content, style='Quote')

        # 保存 Word 文档
        doc.save(output_path)


if __name__ == '__main__':
    layout_word = LayoutWord()
    layout_word.generate_word_document("b.jpg", "gen.docx")
