import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
    
    # 安全与资源限制配置
    MAX_FILE_SIZE_MB = 20  # 严格限制文件大小为20MB
    MAX_PDF_PAGES = 30     # 限制单次最多解析30页PDF，防止DoS
    MAX_TEXT_LENGTH = 8000 # 限制传入大模型的最大字符数
    ENABLE_DATA_MASKING = True # 开启数据脱敏机制
    
    SUPPORTED_FORMATS = ['.pdf', '.xlsx', '.xls', '.docx', '.png', '.jpg', '.jpeg']
    
    SERVER_NAME = "127.0.0.1"
    SERVER_PORT = 7862

config = Config()