import streamlit as st
import base64
from openai import OpenAI

st.write("Hello World")

st.title("Ask GPT using your OpenAPI Key!")

st.header("Enter your OpenAI API Key", divider=True)
api_key = st.text_input("API Key", type="password")

prompt = st.text_input("Image generator: Write your prompt")

# 이미지 생성 버튼
if st.button("Generate Image", type="primary"):
    if not api_key:
        st.error("API Key를 입력하세요!")
    elif not prompt:
        st.error("프롬프트를 입력하세요!")
    else:
        try:
            client = OpenAI(api_key=api_key)

            # 이미지 생성
            img = client.images.generate(
                model="gpt-image-1-mini",
                prompt=prompt)
            image_bytes = base64.b64decode(img.data[0].b64_json)
            # 메모리 상의 이미지 보여주기
            st.image(image_bytes)

        except Exception as e:
            st.error(f"Error: {str(e)}")