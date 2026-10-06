
import time
import streamlit as st
from rag import RagService
import config_data as config


# 应用标题
st.title("服装选择智能客服")
st.divider()                 # 分隔线

# 会话状态，用于存储用户和客服的对话历史
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么能帮你的？"}]

# RAG服务的实例
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 显示对话历史
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入框
prompt = st.chat_input()

# 处理用户输入
if prompt:                  # 当用户输入内容时
    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("AI 正在思考中..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk


        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})


