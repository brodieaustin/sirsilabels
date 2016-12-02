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

    for i in range(1, (len(lines)-1)):
        line = lines[i].strip().replace('/', '')
        line_before = lines[i-1].strip().replace('/', '')
        line_after = lines[i+1].strip().replace('/', '')

        if len(line) > 0:
            print (line)

            #need to group stuff, then split on comma
            #need to look for dewey numbers and put cutter on next line

            if ',' in line:
                line = line.replace(',', ', ')

            if len(line_before) == 0 or line_before == '.folddata':
                results.append({})
                results[r]['category'] = line
                results[r]['item'] = ''

            elif len(line_before) > 0 and len(line_after) > 0:
                #add exceptions for JUV
                if line == 'FICTION':
                        results[r]['category'] += ' ' + line

                else:
                        results[r]['item'] += line

            else:
                results[r]['item'] += line
                r += 1

    return results


#routing and views
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        session.clear()
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

            if request.form['offset']:
                session['offset'] = request.form['offset']

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
