
import os
import json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, BaseMessage, messages_from_dict
from typing import Sequence


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")



class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id       # 会话ID
        self.storage_path = storage_path   # 不同会话id的存储文件所在的文件夹路径
        # 会话id对应的完整文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)


        # 确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)


    def add_messages(self, messages) -> None:
        # Sequence序列 类似列表、元组等
        all_messages = list(self.messages)        # 会话历史消息列表
        all_messages.extend(messages)                 # 合并新老消息

        # 保存会话历史消息到文件
        # 类对象写入文件——> 一堆二进制
        # 为了方便，可以将BaseMessage消息转为字典（借助json字符串写入文件）
        # 官方message_to_dict:单个消息对象（BaseMessage类实例） ——> 字典

        new_messages = [message_to_dict(message)  for message in all_messages]

        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property         # @property装饰器：将messages方法转换为成员属性
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
             return  []


    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)