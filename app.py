from flask import Flask, render_template, request, redirect
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file is in the request
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If user does not select file
        if file.filename == '':
            return 'No selected file'
        if file:
            copies = request.form.get('copies', '1')
            duplex = request.form.get('duplex')

            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Build the lp command with options
            lp_command = ['lp', '-n', copies]
            if duplex:
                lp_command.extend(['-o', 'sides=two-sided-long-edge'])
            lp_command.append(filepath)

            subprocess.run(lp_command)
	    print(lp_command)
            return 'File sent to printer'

    return '''
        <!doctype html>
        <title>Upload PDF for Printing</title>
        <h1>Upload PDF File</h1>
        <form method=post enctype=multipart/form-data>
        <label>PDF File:</label><br>
        <input type=file name=file accept="application/pdf"><br><br>
        <label>Number of Copies:</label><br>
        <input type=number name=copies value="1" min="1"><br><br>
        <label>Double-Sided:</label>
        <input type=checkbox name=duplex value="True"><br><br>
        <input type=submit value=Upload>
        </form>
        '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
