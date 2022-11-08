from flask import Flask, render_template as rt, request as rq, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lpm.db'
db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<Users %r>' % self.id
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def login():
    if rq.method == 'POST':
        log_username = rq.form.get('log_username')
        log_password = rq.form.get('log_password')
        un = db.one_or_404(db.select(User).filter_by(username=log_username))
        if log_username == un.username:
            return rt('test.html')
    else:
        return rt('login.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if rq.method == 'POST':
        new_user = User(
            username = rq.form.get('reg_username'),
            password = rq.form.get('reg_password'),
        )
        db.session.add(new_user)
        db.session.commit()
        return rt('test.html')
    else:
        return rt('register.html')