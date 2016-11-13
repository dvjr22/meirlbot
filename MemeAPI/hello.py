from flask import Flask, jsonify
import os, subprocess, signal
app = Flask(__name__)

data = [
    {
        'id':1,
        'title':'test'
    },
    {
        'id':2,
        'title':'test2'
    }
]

@app.route('/',methods=['GET'])
def hello():
    return jsonify({'data': data})

@app.route('/<int:data_id>',methods=['GET'])
def getData(data_id):
    d = [d for d in data if d['id'] == data_id]
    if len(d) == 0:
        abort(404)
    return jsonify({'data':d[0]})

@app.route('/start/<string:directory>/<string:filename>',methods=['GET'])
def startFile(filename,directory):
    try:
        os.system("python ../%s/%s.py &" % (directory,filename))
    except e as Exception:
        print 'Error %s' % e
        abort(404)
    return "Started %s" % filename

@app.route('/stop/<string:directory>/<string:filename>',methods=['GET'])
def stopFile(filename,directory):
    try:
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if filename in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
    except e as Exception:
        print 'Error %s' % e
        abort(404)
    return "Stopped %s" % filename

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5008, debug=True)
