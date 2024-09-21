from flask import Flask, render_template, request, flash, redirect, url_for
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part.', 'danger')
            return redirect(url_for('upload_file'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file.', 'danger')
            return redirect(url_for('upload_file'))
        if file:
            copies = request.form.get('copies', '1')

            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Build the lp command with options
            lp_command = ['lp', '-n', copies]
            lp_command.append(filepath)

            try:
                subprocess.run(lp_command, check=True)
                # Delete the file after printing
                os.remove(filepath)
                return redirect(url_for('print_success'))
            except subprocess.CalledProcessError as e:
                # Delete the file after printing
                os.remove(filepath)
                flash('Failed to send file to printer. Please try again.', 'danger')
                return redirect(url_for('upload_file'))
    else:
        return render_template('index.html')

@app.route('/success')
def print_success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
