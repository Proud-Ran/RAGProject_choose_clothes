import os
from dotenv import load_dotenv
load_dotenv()



md5_path = "./md5.txt"

# Chroma
collection_name = "RAG"
persist_directory = "./chroma_db"


# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_spliter_char_number = 10000    # 文本分割的阈值


# 检索器的相似度阈值
similarity_threshold = 1   # 检索返回匹配的文档数量


# 嵌入模型
embedding_model_name = "qwen3-embedding:8b"

# 对话模型 —— 这里只存放"配置信息"（字符串/密钥），不创建模型对象
chat_model_name = "mimo-v2.6-flash"                 # 模型的名字（字符串）
chat_api_key = os.getenv("MIMO_API_KEY")            # 模型的 API 密钥
chat_base_url = "https://api.xiaomimimo.com/v1"     # 模型的接口地址



# 会话配置
session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
