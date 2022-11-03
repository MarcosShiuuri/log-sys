from flask import Flask, render_template as rt, request as rq, redirect as rd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lpm.db'
db = SQLAlchemy(app)
db.init_app(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    un = db.Column(db.String, unique=True, nullable=False)
    pw = db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<Users %r>' % self.id
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def login():
    if rq.method == 'POST':
        return rt('login.html')
    else:
        return rt('login.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if rq.method == 'POST':
        username = rq.form.get('reg_username')
        password = rq.form.get('reg_password')
        new_user = Users(un=username, pw=password)
        db.session.add(new_user)
        db.session.commit()
        return rt('test.html')
    else:
        return rt('register.html')