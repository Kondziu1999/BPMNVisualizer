from flask import Flask, request, send_file
from flask_cors import CORS
import os

from engine import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'
cors = CORS(app, resources=r'/*', headers='Content-Type')


@app.route("/")
def home():
    response = {"status": "OK"}
    return response


@app.route('/generate', methods=['GET', 'POST'])
def get_image():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            cols = request.form['columns'].split(',')
            threshold = int(request.form['tsh'])
            filepath = os.path.join('./upload', file.filename)
            file.save(filepath)
            draw_and_save(filepath, cols, threshold)
            response = send_file('simple_process_model.png', mimetype='image/png')
            return response

        return "Bad request", 400
    return "Bad request", 400


if __name__ == "__main__":
    app.run(debug=True)