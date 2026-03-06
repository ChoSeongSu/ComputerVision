# import streamlit as st

# st.title("Hello World")

# st.divider()
# st.write("안녕하세요 샘플 봇 입니다.")

# name = st.text_input("당신의 이름은 무엇입니까")
# button_clik = st.button("입력완료")

# if button_clik:
#     st.write(name + "님 반갑습니다.")

import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)