import streamlit as st
from openai import OpenAI

st.title("💬 Chat with gpt-5-mini")

# API Key 확인
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.error("먼저 API Key를 입력하는 페이지에서 API Key를 설정하세요!")
    st.stop()

client = OpenAI(api_key=st.session_state.api_key)

# 대화 저장소 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear 버튼
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# 이전 대화 모두 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 출력
    st.chat_message("user").markdown(prompt)

    # 메모리에 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # OpenAI Responses API 호출
    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=st.session_state.messages,
        )
        assistant_reply = response.choices[0].message.content

    except Exception as e:
        assistant_reply = f"⚠️ 오류 발생: {e}"

    # Assistant 메시지 출력
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    # 메모리에 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )
