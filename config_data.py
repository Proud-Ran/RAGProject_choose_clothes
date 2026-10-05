
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

