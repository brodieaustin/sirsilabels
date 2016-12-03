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
    for i in range(1, len(lines)):

        #for each line get line, prev line, and and next line
        line = lines[i].strip().replace('/', '')
        prev_line = lines[i-1].strip().replace('/', '')

        #make sure there is a next line before trying to capture it
        if i < (len(lines)-1) :
            next_line = lines[i+1].strip().replace('/', '')
        else:
            next_line = ''

        if len(line) > 0:

            #if the first line capture it as a category
            if len(prev_line) == 0 or prev_line == '.folddata':
                results.append({})
                results[r]['category'] = line
                results[r]['item'] = ''

            elif len(prev_line) > 0 and len(next_line) > 0:
                #Add line to previous line if current line is Fiction and previous is Science
                if line == 'FICTION':
                    if prev_line == 'SCIENCE':
                        results[r]['category'] += ' ' + line

                else:
                        results[r]['item'] += line

            else:
                results[r]['item'] += line
                r += 1

    return results


#routing and views
@app.route('/', methods=['GET'])
def upload_file():
    return render_template('upload.html')

@app.route('/labels/', methods=['GET', 'POST'])
def view_labels(offset=None):
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file in the request')
            return redirect(url_for('upload_labels'))

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('upload_labels'))

        if file and allowed_file(file.filename):
            #read lines into array
            labels = parse_file(file)

            if request.form['offset']:
                print request.form['offset']
                offset = request.form['offset']
            else:
                offset = None

            return render_template('labels.html', labels=labels, offset=offset)


    else:
        flash('Upload a file to view labels')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run()
