import os
from flask import Flask, render_template, request, redirect, url_for
import svm 

app = Flask(__name__)

# Create required folders
for folder in ['static/uploads', 'static/LineSweep_Results', 'static/OCR_Results']:
    if not os.path.exists(folder):
        os.makedirs(folder)

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join('static/uploads', file.filename)
        file.save(filepath)
        return render_template('template.html', filename=file.filename)

@app.route('/process_ocr', methods=['POST'])
def process_ocr():
    # Find newest file
    upload_folder = 'static/uploads'
    files = [f for f in os.listdir(upload_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return render_template('template.html', result="No Data Found")
    
    files.sort(key=lambda x: os.path.getmtime(os.path.join(upload_folder, x)))
    latest_file = files[-1]

    # Run AI Logic
    result = svm.svm_algo() 

    return render_template('template.html', result=result, filename=latest_file)

@app.route('/reload')
def reload():
    # Clean uploads for fresh start
    for f in os.listdir('static/uploads'):
        os.remove(os.path.join('static/uploads', f))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)