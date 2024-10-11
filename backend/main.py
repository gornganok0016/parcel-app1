
from flask import Flask, jsonify
from flask import Flask, request, jsonify, render_template
import os
import pandas as pd  
from model import read_name_from_image, crop_and_read_names, save_to_csv, count_names_in_csv

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_FILE = 'D:\POSTOAPP2\backend\names.csv' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            if not (file.filename.endswith('.jpg') or file.filename.endswith('.png')):
                return jsonify({'error': 'File format not supported'}), 400

            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            detected_names, boxes = read_name_from_image(image_path)

            if detected_names:
                cropped_names = crop_and_read_names(image_path, boxes)
                save_to_csv(cropped_names)

                return jsonify({
                    'detected_names': detected_names,
                    'cropped_names': cropped_names,
                    'name_counts': count_names_in_csv().to_dict(orient='records')
                })
            else:
                return jsonify({'message': 'No names detected.'}), 404

        return render_template('admin.html')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat')
def chat_page():
    return render_template('chatbot.html')  # เรนเดอร์ไฟล์ HTML ของ Chatbot

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    
    # ตรวจสอบว่าคำถามมีอยู่ใน CSV หรือไม่
    if question:
        if check_question_in_csv(question):
            answer = f"The question '{question}' is found in the CSV."
        else:
            answer = f"The question '{question}' is not found in the CSV."
    else:
        answer = "Please ask a valid question."
    
    return jsonify({'answer': answer})

def check_question_in_csv(question):
    # อ่านข้อมูลจากไฟล์ CSV
    try:
        df = pd.read_csv(CSV_FILE)  # อ่านไฟล์ CSV
        print(df.head())  # แสดงข้อมูลที่อ่านได้จาก CSV สำหรับการดีบัก
        # ตรวจสอบว่าชื่ออยู่ในคอลัมน์ 'name'
        return question in df['name'].values
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False
    
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
