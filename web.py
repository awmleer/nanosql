from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')




app.secret_key = b'\x99SVK\xcd\x80\xf5-\x87B\xd3\xe7\xfbFD;\x18Ow\xc1K\xe9&\xe7'
if __name__ == '__main__':
    app.run(debug=True)