from applications import app

if __name__ == '__main__':
    print(app.config)
    print("服务启动→0.0.0.0:3007")
    # print("功能1：OCR识别/demo/ocr")
    print("功能2：PDF转换/demo/pdf")
    print("功能3：word生成/demo/word")
    app.run(port=3007)