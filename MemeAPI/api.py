from flask import Flask, jsonify
import json
import os, subprocess, signal
app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return "The API is up and running!"

@app.route('/<int:data_id>',methods=['GET'])
def getData(data_id):
    d = [d for d in data if d['id'] == data_id]
    if len(d) == 0:
        abort(404)
    return jsonify({'data':d[0]})

@app.route('/start/<string:directory>/<string:filename>',methods=['GET'])
def startFile(filename,directory):
    try:
        os.system("python ../%s/%s.py > %soutput.txt &" % (directory,filename,filename))
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

@app.route('/log/return/',methods=['GET'])
def getLog():
    with open('systemTest.log','r') as f:
        f.seek(0,2) # Seek the EOF
        fsize = f.tell() # get the size of the chunk
        f.seek (max (fsize-1024,0),0) # Set position at last n chars
        lines = f.readlines() # Read to the end
    lines = lines[-20:] # Concatenate the last 20 together
    return json.dumps(lines)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5008, debug=True)
