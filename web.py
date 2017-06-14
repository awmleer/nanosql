from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import core
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute/',methods=['POST'])
def execute():
    sql=request.form['sql']
    result=core.execute(sql)
    if type(result['payload'])==str:
        result['type']='str'
    if type(result['payload'])==dict:
        result['type']='dict'
    return render_template('result.html',result=result,sql=sql)



app.secret_key = b'\x99SVK\xcd\x80\xf5-\x87B\xd3\xe7\xfbFD;\x18Ow\xc1K\xe9&\xe7'
if __name__ == '__main__':
    app.run(debug=True)