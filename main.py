import os
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["GRADIO_TELEMETRY_ENABLED"] = "False"
os.environ["GRADIO_SERVER_NAME"] = "127.0.0.1"

import gradio as gr
import pandas as pd
from datetime import datetime
import traceback
from llm_client import AuditLLMClient
from document_parser import DocumentParser
from security_utils import SecurityManager
from config import config

class AuditDocExtractor:
    def __init__(self):
        self.llm_client = AuditLLMClient()
        self.doc_parser = DocumentParser()

    def create_interface(self):
        with gr.Blocks() as demo:
            gr.Markdown("## 📊 AI-Audit-Doc-Extractor 智能审计文档提取助手 \n*(已开启企业级数据安全与合规防护)*")
            
            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(label="上传审计文档 (上限20MB)", file_count="multiple", type="filepath")
                    doc_type = gr.Dropdown(
                        choices=["自动识别", "资产负债表", "利润表", "现金流量表", "发票", "合同"],
                        value="自动识别", label="文档类型"
                    )
                    analysis_mode = gr.Radio(
                        choices=["完整审计分析", "快速数据提取", "风险扫描"],
                        value="完整审计分析", label="分析模式"
                    )
                    process_btn = gr.Button("🚀 开启安全分析", variant="primary")
                
                with gr.Column(scale=2):
                    with gr.Tabs():
                        with gr.TabItem("📋 审计摘要"):
                            summary_output = gr.JSON(label="结构化分析结果")
                        with gr.TabItem("⚠️ 风险提示"):
                            risk_output = gr.Dataframe(headers=["等级", "描述"], label="风险识别清单")
                        with gr.TabItem("📝 工作底稿"):
                            working_paper = gr.Textbox(label="审计工作底稿（已脱敏处理）", lines=15)
            
            process_btn.click(
                fn=self.process_documents,
                inputs=[file_input, doc_type, analysis_mode],
                outputs=[summary_output, risk_output, working_paper]
            )
        return demo

    def process_documents(self, files, doc_type, mode):
        if not files:
            return {"error": "未上传文件"}, pd.DataFrame(), ""
            
        results = []
        all_risks = []
        working_papers = []
        
        for file_path in files:
            safe_filename = SecurityManager.sanitize_filename(file_path)
            try:
                # 1. 前置安全检查
                SecurityManager.check_file_security(file_path, config.MAX_FILE_SIZE_MB)
                
                # 2. 解析文档
                parsed = self.doc_parser.parse(file_path)
                raw_text = parsed['text']
                
                # 3. 数据脱敏清洗
                if config.ENABLE_DATA_MASKING:
                    safe_text = SecurityManager.mask_sensitive_data(raw_text)
                else:
                    safe_text = raw_text
                
                # 4. LLM 安全分析
                result = self.llm_client.analyze_document(safe_text, doc_type, mode)
                results.append(result)
                
                if 'risk_alerts' in result:
                    all_risks.extend(result['risk_alerts'])
                    
                # 5. 生成底稿
                paper = self._generate_working_paper(safe_filename, result, parsed)
                working_papers.append(paper)
                
            except Exception as e:
                error_details = traceback.format_exc()
                print(f"[{datetime.now()}] 错误详情:\n{error_details}")
                results.append({"error": f"处理失败: {str(e)}", "file": safe_filename})
                print(f"[{datetime.now()}] 内部错误拦截: {traceback.format_exc()}") # 仅在后台打印真实错误

        risk_df = pd.DataFrame(all_risks) if all_risks else pd.DataFrame(columns=["等级", "描述"])
        paper_text = "\n\n".join(working_papers)
        
        return {"执行结果": results}, risk_df, paper_text

    def _generate_working_paper(self, filename: str, result: dict, parsed: dict) -> str:
        paper = f"""[机密] 审计工作底稿
======================================================
文档名称: {filename}
文档类型: {parsed.get('type', '未知')}
分析日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}
安全声明: 原始数据已通过安全脱敏层处理
------------------------------------------------------
一、审计摘要
{result.get('summary', '未提取到有效信息')}

二、关键数据提取\n"""
        for item in result.get('key_items', []):
            paper += f"- {item.get('科目', 'N/A')}: {item.get('金额', 'N/A')} ({item.get('占比', 'N/A')})\n"
            
        paper += "\n三、风控与合规警示\n"
        for risk in result.get('risk_alerts', []):
            paper += f"- [{risk.get('等级', '中')}] {risk.get('描述', 'N/A')}\n"
            
        paper += f"\n四、审计结论及建议\n{result.get('audit_conclusion', 'N/A')}\n======================================================"
        return paper

if __name__ == "__main__":
    app = AuditDocExtractor()
    demo = app.create_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=config.SERVER_PORT,
        share=False,
        show_error=False,
        theme=gr.themes.Soft()
    )
