import os

from flask import Flask, request, redirect

from detector import calculate_sequence


WEB_HOST = os.environ.get('WEB_HOST', 'localhost')
WEB_PORT = int(os.environ.get('WEB_PORT', '80'))
ALLOWED_EXTENSIONS = {'ogv', 'mp4', 'avi'}
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return redirect(request.url)
        elif allowed_file(file.filename):
            filename = 'video.mp4'
            file.save(filename)
            calculate_sequence(filename, 'static/sequence.jpg')
            os.remove(filename)
            return '''
                <title>Detection Sequence</title>
                <form method=get>
                  <input type=submit value='Try again'>
                </form>
                <img style='margin-top:50px' src='static/sequence.jpg'/>
            '''
    return '''
        <title>Upload video</title>
        <h1>Upload video</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
    '''

if __name__ == "__main__":
    app.run(host=WEB_HOST, port=WEB_PORT)
