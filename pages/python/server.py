from flask import *
import subprocess
import cctvinator as cn
app = Flask(__name__)


@app.route('/getVideo')
def processVideo():

    return cn.processVideo(request.args.get('path'))

@app.route('/openFile')
def open():
    
    subprocess.Popen('explorer "D:\Projects\CCtvinator\pages\summarized_videos"')
    return "hi"

if __name__ == '__main__':
    app.run(debug=True)
