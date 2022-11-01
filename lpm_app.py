from flask import Flask, render_template as rt, request as rq, redirect as rd

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def login():
    if rq.method == 'POST':
        username = rq.form.get('username')
        password = rq.form.get('password')
        return rt('test.html', us=username, pw=password)
    else:
        return rt('login.html')