"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str:str):
    """检查传入的md5字符串是否已经被处理过了"""
    if not os.path.exists(config.md5_path):           # if进入表示文件不存在，那肯定没有处理过这个md5字符串
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()                 # 处理字符串前后的空格和回车
            if line == md5_str:
                return True

        return False



def save_md5(md5_str:str):
    """将传入的md5字符串，记录到文件内保存"""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str : str, encoding = 'utf-8'):
    """将传入的字符串转换为md5字符串"""

    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding = encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()               # 得到一个md5对象
    md5_obj.update(str_bytes)             # 更新内容（传入即将要转换的字节数组）
    md5_hex = md5_obj.hexdigest()         # 得到md5的16进制字符串

    return md5_hex



class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)  # 如果数据库文件夹不存在，就创建一个，存在就直接跳过
        self.chroma = Chroma(
            collection_name = config.collection_name,                      # 数据库的表名
            embedding_function = OllamaEmbeddings(model="qwen3-embedding:8b"),
            persist_directory = config.persist_directory,                  # 数据库的本地存储文件夹
        )                      # 向量存储的实例，Chroma向量数据库
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,                    # 分割后的文本段最大长度
            chunk_overlap = config.chunk_overlap,              # 连续文本段之间的字符重叠数量
            separators = config.separators,                    # 自然段落划分的符号
            length_function=len,                               # 使用Python自带的len函数做长度统计的依据

        )                     # 文本分割器的实例，用于将文本分割为向量


    def upload_by_str(self,data:str, filename):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        # 先得到传入字符串的md5值
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        if len(data) > config.max_spliter_char_number:
            knowledge_chunks:list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "牛批"
        }
        self.chroma.add_texts(              # 将内容向量化，存入数据库中
            knowledge_chunks,
            metadata = [metadata for _ in knowledge_chunks]

        )

        # 记录md5值
        save_md5(md5_hex)

        return "[成功添加]内容已存入向量知识库"




if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str("牛批","testfile")
    print(r)



