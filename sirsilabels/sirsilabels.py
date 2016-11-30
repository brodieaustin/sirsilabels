import os
from flask import Flask, flash, session, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import secrets

#configs
ALLOWED_EXTENSIONS = set(['txt'])

#initialize app
app = Flask(__name__)

#secret key is secret
app.secret_key = secrets.SECRET_KEY

#helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def parse_file(file):
    lines = file.readlines()

    #initialize dictionary for results
    results = [];
    r = 0

    #loop through results and pass into results dictionary
    for i in range(0, len(lines)):
        l = lines[i].strip().replace('/', '')

        if l != '.folddata' and len(l) > 1:

            if i % 2:
                results.append({})
                results[r]['number'] = l

            else:
                results[r]['category'] = l
                r += 1

    return results


#routing and views
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file in the request')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #read lines into array
            session['labels'] = parse_file(file)

            return redirect(url_for('view_labels'))

    return render_template('upload.html')

@app.route('/labels/')
def view_labels():
    if session.get('labels'):
        return render_template('labels.html')

    else:
        flash('Upload a file to view labels')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run()
