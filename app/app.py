import os
from flask import Flask, flash, session, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

#configs
UPLOAD_FOLDER = './media/uploads'
ALLOWED_EXTENSIONS = set(['txt'])

#initialize app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#secret key is secret
app.secret_key = 'EoCwMDIq44AN#MasYV5U7@ig'

#helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('make_labels',
                                    filename=filename))

    return render_template('upload.html')

@app.route('/labels/<filename>')
def make_labels(filename):
    #open file to parse
    with open(os.path.join(UPLOAD_FOLDER, filename)) as f:

        #read lines into array
        lines = f.readlines()

        #initialize dictionary for results
        results = {'data': []};
        r = 0

        #loop through results and pass into results dictionary
        for i in range(0, len(lines)):
            l = lines[i].strip().replace('/', '')

            if l != '.folddata' and len(l) > 1:

                if i % 2:
                    results['data'].append({})
                    results['data'][r]['number'] = l

                else:
                    results['data'][r]['category'] = l
                    r += 1

    return render_template('labels.html', results=results)
