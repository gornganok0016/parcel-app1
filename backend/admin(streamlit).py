import streamlit as st
import requests
import os

# กำหนดโฟลเดอร์สำหรับการอัปโหลด
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# สร้างหน้า Admin Upload
st.title("Admin Upload")

# รับไฟล์จากผู้ใช้
uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'png'])

if uploaded_file is not None:
    # บันทึกไฟล์ที่อัปโหลด
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ส่งไฟล์ไปยังเซิร์ฟเวอร์ Flask เพื่อประมวลผล
    response = requests.post('http://localhost:5000/admin', files={'file': uploaded_file})

    if response.ok:
        data = response.json()
        st.success('Detected Names: ' + ', '.join(data['detected_names']))
        st.success('Cropped Names: ' + ', '.join(data['cropped_names']))
    else:
        st.error('Error: ' + (data.get('error') or data.get('message', 'Unknown error')))
