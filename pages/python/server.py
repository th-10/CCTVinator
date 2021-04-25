from flask import *
import subprocess
import webbrowser

import cctvinator as cn
app = Flask(__name__)


@app.route('/getVideo')
def processVideo():

    return cn.processVideo(request.args.get('path'))

@app.route('/openFile')
def open():
    
    subprocess.Popen('explorer "D:\Projects\CCtvinator\pages\summarized_videos"')
    return "hi"

@app.route("/openCloud")
def openCloudinary():
    url = request.args.get('link')
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    webbrowser.get(chrome_path).open(url)
    return "Q"




if __name__ == '__main__':
    app.run(debug=True)
