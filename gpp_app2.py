import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="gpt-5-mini demo")

st.title("gpt-5-mini 질의응답 데모")

# 1. API Key를 session_state에 저장
st.subheader("1. OpenAI API Key 입력")

api_key = st.text_input(
    "OpenAI API Key를 입력하세요",
    type="password",
    key="api_key"   # 🔹 이 key 덕분에 session_state["api_key"]에 자동 저장됨
)

st.write("---")

st.subheader("2. 질문 입력")
question = st.text_area("gpt-5-mini에게 물어볼 내용을 적어보세요:", height=150)


# 3. 질문이 같으면 결과를 재사용하도록 캐시
@st.cache_data(show_spinner=True)
def ask_gpt_cached(question: str) -> str:
    """
    같은 question으로 다시 호출되면
    OpenAI API를 다시 부르지 않고
    이전에 저장된 답을 그대로 돌려준다.
    """
    api_key_inner = st.session_state.get("api_key", "")
    client = OpenAI(api_key=api_key_inner)

    resp = client.chat.completions.create(
        model="gpt-5-mini",   # 과제 요구 사항
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
    )
    return resp.choices[0].message.content


# 4. 버튼 눌렀을 때 동작
if st.button("질문 보내기"):
    if not api_key:
        st.error("먼저 OpenAI API Key를 입력하세요.")
    elif not question.strip():
        st.error("질문을 입력하세요.")
    else:
        answer = ask_gpt_cached(question)
        st.markdown("### gpt-5-mini의 응답")
        st.write(answer)
