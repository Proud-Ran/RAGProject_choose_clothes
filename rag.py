from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_ollama import OllamaEmbeddings
from vector_stores import VectorStoreService
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from file_history_store import get_history

load_dotenv()

def print_prompt(prompt):
    print("="*50)
    print(prompt.to_string())
    print("="*50)

    return prompt

class RagService(object):

    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=OllamaEmbeddings(model=config.embedding_model_name),
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，"
                 "简洁和专业地回答用户问题。参考资料:{context}。"),
                ("system", "并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问:{input}")
            ]
        )

        self.chat_model = ChatOpenAI(
            model=config.chat_model_name,
            api_key=config.chat_api_key,
            base_url=config.chat_base_url,
        )

        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"

            formated_str = ""
            for doc in docs:
                formated_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formated_str

        def format_for_retriever(value):

            return value["input"]


        chain = (
            RunnablePassthrough.assign(
                context=RunnableLambda(format_for_retriever) | retriever | format_document
            )
            | self.prompt_template
            | print_prompt
            | self.chat_model
            | StrOutputParser()
        )
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",

        )

        return conversation_chain



if __name__ == "__main__":
    # session id 配置
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }

    res = RagService().chain.invoke({"input": "针织衫如何保养？"}, session_config)
    print(res)



