from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file:
            # Send the file to the second container (assuming second container's service name is 'processor')
            files = {'file': file.read()}
            response = requests.post('http://processor-service:5000/process', files=files)

            if response.status_code == 200:
                flash('File successfully uploaded and processed')
                return redirect(url_for('index'))
            else:
                flash('File upload failed')
        else:
            flash('No file selected')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
