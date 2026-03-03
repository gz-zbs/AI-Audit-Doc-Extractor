import re
import os
from config import config

class SecurityManager:
    @staticmethod
    def check_file_security(filepath: str, max_size_mb: int) -> bool:
        """检查文件大小和基础安全性"""
        if not os.path.exists(filepath):
            raise FileNotFoundError("文件不存在或上传失败")
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in config.SUPPORTED_FORMATS:
            raise ValueError(f"安全拦截：不支持的文件格式 {ext}，仅支持 {', '.join(config.SUPPORTED_FORMATS)}")
            
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            raise ValueError(f"安全拦截：文件大小 ({file_size_mb:.1f}MB) 超出系统限制 ({max_size_mb}MB)。")
        return True

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """防止路径穿越漏洞 (Path Traversal)"""
        return os.path.basename(filename)

    @staticmethod
    def mask_sensitive_data(text: str) -> str:
        """审计数据脱敏：隐藏身份证、手机号和部分银行卡号"""
        if not text:
            return text
            
        # 脱敏 18位身份证号
        text = re.sub(r'\d{6}[\s]?\d{8}[\s]?\d{3}[\dXx]', '***IDCARD***', text)
        # 脱敏 11位手机号
        text = re.sub(r'1[3-9]\d{1}[\s\-]?\d{4}[\s\-]?\d{4}', '***PHONE***', text)
        # 脱敏 银行卡号 (保留后四位)
        text = re.sub(r'(?:\d[\s\-]?){12,15}(\d{4})', r'***BANKCARD-尾号\1***', text)
        
        return text