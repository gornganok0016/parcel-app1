import streamlit as st
import os
import pandas as pd
from model import read_name_from_image, crop_and_read_names, save_to_csv, count_names_in_csv

# ตั้งค่า
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CSV_FILE = 'D:\POSTOAPP2\backend\names.csv'

# หน้าแรก
st.title("Welcome to the Name Detection App")
st.markdown("[Go to Admin Page](#admin-page)")
st.markdown("[Go to Chatbot](#chatbot)")

# หน้า Admin
st.markdown("## Admin Page")
uploaded_file = st.file_uploader("Upload an image...", type=['jpg', 'png'])
if uploaded_file is not None:
    # บันทึกไฟล์ที่อัปโหลด
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    detected_names, boxes = read_name_from_image(image_path)
    
    if detected_names:
        cropped_names = crop_and_read_names(image_path, boxes)
        save_to_csv(cropped_names)
        
        st.success("Detection Complete!")
        st.write("Detected Names:", detected_names)
        st.write("Cropped Names:", cropped_names)
        st.write("Name Counts:", count_names_in_csv().to_dict(orient='records'))
    else:
        st.error("No names detected.")

# หน้า Chatbot
st.markdown("## Chatbot")
question = st.text_input("Ask a name...")
if st.button("Submit"):
    if question:
        if check_question_in_csv(question):
            answer = f"The question '{question}' is found in the CSV."
        else:
            answer = f"The question '{question}' is not found in the CSV."
    else:
        answer = "Please ask a valid question."
    
    st.write("Answer:", answer)

# ฟังก์ชันสำหรับตรวจสอบคำถามใน CSV
def check_question_in_csv(question):
    try:
        df = pd.read_csv(CSV_FILE)
        return question in df['name'].values
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return False
