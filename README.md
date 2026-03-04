# 📊 AI-Audit-Doc-Extractor 智能审计文档提取助手
在使用之前一定要先获得api，大模型api，目前本项目所有测试都在在智谱清言模型进行测试，可以在项目根目录.env文件配置环境中配置自己选用的模型

智谱大模型api-->注册并实名领取免费ai大模型api：https://www.bigmodel.cn/invite?icode=noj0WqsdOw5wJyOkb5h210jPr3uHog9F4g5tjuOUqno%3D

## ✨ 核心特性

- **多格式支持**：PDF、Excel、Word、图片（OCR自动识别）
- **智能分析**：基于DeepSeek等LLM自动提取关键财务指标与勾稽关系
- **风险扫描**：自动识别财务数据异常与合规风险（高/中/低分级）
- **数据安全**：内置身份证、手机号、银行卡号自动脱敏
- **资源保护**：严格限制文件大小（20MB）、页数（30页）、文本长度（8000字符）

  ## 🛠️ 技术栈

- **Web框架**: Gradio 4.44.0
- **LLM接口**: OpenAI SDK（兼容DeepSeek API）
- **文档解析**: PyMuPDF、python-docx、pandas、EasyOCR
- **工程化**: 重试机制(tenacity)、数据验证(pydantic)

## 🚀 快速开始
### 环境要求

- Python 3.9+
- 16GB+ 内存（OCR模型加载需要）
- DeepSeek API Key（或其他兼容OpenAI的API）
### 安装步骤
1. **克隆仓库**
   ```bash
   git clone https://github.com/gz-zbs/AI-Audit-Doc-Extractor.git

🚀 使用方法

在项目根目录下运行：

创建虚拟环境
在PowerShell或CMD中：
```bash
python -m venv venv
```
### Windows
```bash
venv\Scripts\activate
```
### macOS/Linux
```bash
source venv/bin/activate
```

安装依赖
```bash
pip install -r requirements.txt
```

配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

启动服务
```bash
python main.py
```
访问 http://127.0.0.1:7862 即可使用

## 📖 使用说明
1. **上传文档**
 
   支持批量上传，单文件上限20MB
3. **选择类型**
 
   支持自动识别或手动指定（资产负债表/利润表/现金流量表/发票/合同）
4. **分析模式**
 
   完整审计分析：生成摘要、提取数据、风险识别、勾稽校验
 
   快速数据提取：仅提取关键财务数据
 
   风险扫描：重点识别异常与合规风险
5. **查看结果**
 
   审计摘要（结构化JSON）
 
   风险清单（分级表格）
 
   工作底稿（脱敏处理后的文本）

## 🏗️ 项目结构
```bash
AI-Audit-Doc-Extractor/
├── main.py                 # 程序入口（Gradio界面）
├── config.py               # 全局配置（安全限制、API设置）
├── document_parser.py      # 文档解析引擎
├── llm_client.py          # LLM调用与安全提示管理
├── security_utils.py      # 数据脱敏与文件安全检查
├── requirements.txt       # 依赖清单
├── .env.example          # 环境变量模板
└── .gitignore            # Git排除规则
```

## 🔒 安全说明
```⚠️ 重要提示：
 
生产环境部署前务必修改  config.py  中的  SERVER_NAME  和启用HTTPS
 
API密钥仅存储在本地  .env  文件，切勿提交到Git仓库
 
系统已内置防Prompt注入攻击的安全指令
 
敏感数据（身份证、手机号、银行卡）会自动脱敏处理
```

## ⚙️ 配置说明
```配置项	默认值	说明	
`MAX_FILE_SIZE_MB`	20	单文件大小限制	
`MAX_PDF_PAGES`	30	PDF最大解析页数	
`MAX_TEXT_LENGTH`	8000	传入LLM的最大字符数	
`ENABLE_DATA_MASKING`	True	是否开启数据脱敏	
```
## 🤝 贡献指南
```欢迎提交Issue和PR！请确保：
 
代码符合PEP8规范
 
新增功能包含安全边界检查
 
敏感操作添加日志记录
```

## 🙏 致谢
```
感谢所有为这个项目做出贡献的开发者和用户！

如果您觉得这个项目对您有帮助，请考虑给我一个 ⭐ Star！

开始您的 AI 创作之旅吧！ 🚀✨
```

