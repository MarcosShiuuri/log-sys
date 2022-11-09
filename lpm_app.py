from flask import Flask, render_template as rt, request as rq, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lpm.db'
db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.id

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(35), nullable=False)
    project_desc = db.Column(db.String(350), nullable=False)
    def __repr__(self):
        return '<Projects %r>' % self.id
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def login():
    if rq.method == 'POST':
        log_username = rq.form.get('log_username')
        log_password = rq.form.get('log_password')
        user = db.one_or_404(db.select(User).filter_by(username=log_username),
                            description=f"No username '{log_username}' found.")
        if log_password == user.password:
            return rt('pm.html', user=log_username)
        else: return rt('test.html')
    else: return rt('login.html')

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