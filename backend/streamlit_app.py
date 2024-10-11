import streamlit as st
import requests

st.title("Welcome to the Streamlit App!")

# โค้ด Streamlit ของคุณจะไปที่นี่
# เช่น การแสดงปุ่มให้ผู้ใช้สามารถถามคำถาม

question = st.text_input("Ask a question:")

if st.button("Submit"):
    if question:
        # ส่งคำถามไปยัง Flask API
        response = requests.post('http://127.0.0.1:5000/chat', json={'question': question})
        if response.status_code == 200:
            answer = response.json().get('answer')
            st.write(answer)
        else:
            st.write("Error:", response.json().get('error', 'Unknown error occurred.'))
    else:
        st.write("Please ask a valid question.")
