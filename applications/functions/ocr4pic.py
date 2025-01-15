from . import function_bp
import json
from flask import request
from applications.functions.task import OCRWebUtils

processor = OCRWebUtils()


@function_bp.route("/ocr", methods=["POST"])
def ocr():
    if request.method == "POST":
        img_str = request.get_json().get("file", None)
        # print(img_str)
        # print(type(img_str))
        ocr_res = processor(img_str)
        ocr_res = json.loads(ocr_res)
        # total_elapse = ocr_res.get("total_elapse")
        # elapse_part = ocr_res.get("elapse_part")
        # rec_res = ocr_res.get("rec_res")
        # det_boxes = ocr_res.get("det_boxes")
        # rec_res = json.loads(rec_res)
        # for res in rec_res:
        #     print(res)
        # print(len(rec_res), len(det_boxes))
        # for item, box in zip(rec_res, det_boxes):
        #     print(item, box)
        # with open("res.json", "w", encoding="utf-8") as F:
        #     json.dump({"rec_res": rec_res, "det_boxes": det_boxes}, F, ensure_ascii=False)
        # json2pdf({"rec_res": rec_res, "det_boxes": det_boxes})
        return ocr_res
