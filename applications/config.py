import logging


class BaseConfig:  # 基本配置

    STATIC = 'static'

    TEMPLATES = 'templates'

    SUPER_ADMIN = 'super_admin'  # 超级管理员

    SYSTEM_ADMIN = 'system_admin'  # 系统管理员

    UPLOADED_PICTURE = 'static/upload/picture'  # 上传图像存储位置

    UPLOADED_FILE = 'static/upload'  # 上传文件存储位置

    UPLOADED_FILES_ALLOW = ['png', 'jpg', 'jpeg', 'gif', 'doc', 'pdf']  # 允许上传的文件格式

    LOG_LEVEL = logging.WARN  # 默认日志等级
