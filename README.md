# ocr-pwl(pdf-with-layout) 项目

## 项目简介
本项目采用BS架构，后端使用Flask框架，前端使用HTML+JavaScript技术，主要功能是将图像转换为PDF文件，并对图像进行版面分析识别，最终输出Word格式的文档。

## 功能特性
- 图像转PDF：支持上传图像文件并将其转换为PDF格式。
- 版面分析与识别：对图像中的文字和布局进行分析，生成结构化的Word文档。
- 前后端分离：采用现代Web开发模式，前后端通过API接口交互。

## 重要说明
本项目主要依赖RapidAI下智能文档套件,制作并实现上述功能
- Rapid Table https://github.com/RapidAI/RapidTable
- Rapid OCR https://github.com/RapidAI/RapidOCR
- Rapid Layout https://github.com/RapidAI/RapidLayout

## 环境依赖
确保安装以下环境依赖：
- Python 3.8+
- Flask 框架
- 其他Python库（如opencv python-docx reportlab等）

## 安装步骤
1. 克隆仓库：
   `git clone https://github.com/SunpcInuse/ocr_pwl.git`
2. cd ocr_pwl
3. pip install -r requirements.txt
4. python dev.py  # 开发者模式
