from flask import *
import cctvinator as cn
app = Flask(__name__)


@app.route('/getVideo')
def processVideo():

    return cn.processVideo(request.args.get('path'))


if __name__ == '__main__':
    app.run(debug=True)
