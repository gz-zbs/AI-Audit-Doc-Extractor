import fitz  # PyMuPDF
import pandas as pd
import io
import docx
from typing import Dict, Any
from config import config

class DocumentParser:
    def __init__(self):
        self._ocr_reader = None

    def parse(self, filepath: str) -> Dict[str, Any]:
        ext = filepath.lower().split('.')[-1]
        
        with open(filepath, 'rb') as f:
            file_bytes = f.read()

        if ext == 'pdf':
            return self._parse_pdf(file_bytes)
        elif ext in ['xlsx', 'xls']:
            return self._parse_excel(file_bytes)
        elif ext == 'docx':
            return self._parse_word(filepath)
        elif ext in ['png', 'jpg', 'jpeg']:
            return self._parse_image(file_bytes)
        else:
            raise ValueError(f"系统不接受该类型文件: {ext}")
    
    @property
    def ocr_reader(self):
        if self._ocr_reader is None:
            import easyocr # 延迟导入
            print("首次处理图片，正在初始化 OCR 模型，请稍候...")
            self._ocr_reader = easyocr.Reader(['ch_sim', 'en'])
        return self._ocr_reader
        
    def _parse_pdf(self, file_bytes: bytes) -> Dict[str, Any]:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_content = []
        # 安全限制：最多解析设定页数
        limit_pages = min(len(doc), config.MAX_PDF_PAGES)
        for page_num in range(limit_pages):
            page = doc[page_num]
            text_content.append(f"--- 第{page_num+1}页 ---\n{page.get_text()}")
        
        warning = "\n[系统提示：文档超长，已截断处理]" if len(doc) > config.MAX_PDF_PAGES else ""
        return {"type": "pdf", "text": "\n".join(text_content) + warning}

    # （Excel 和 Word 的解析逻辑与上一版类似，但在开头加入限制）
    def _parse_excel(self, file_bytes: bytes) -> Dict[str, Any]:
        df_dict = pd.read_excel(io.BytesIO(file_bytes), sheet_name=None, nrows=2000) # 最多读取2000行
        text_content = []
        for sheet_name, df in df_dict.items():
            text_content.append(f"表名：{sheet_name}\n{df.to_string()}")
        return {"type": "excel", "text": "\n".join(text_content)[:config.MAX_TEXT_LENGTH]}

    def _parse_word(self, filepath: str) -> Dict[str, Any]:
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return {"type": "word", "text": text[:config.MAX_TEXT_LENGTH]}

    def _parse_image(self, file_bytes: bytes) -> Dict[str, Any]:
        # 调用 self.ocr_reader 时自动触发初始化
        result = self.ocr_reader.readtext(file_bytes)
        text = "\n".join([item[1] for item in result])
        return {"type": "image", "text": text[:config.MAX_TEXT_LENGTH]}