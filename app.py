from flask import Flask, render_template as rt, request as rq
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lpm.db'
db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.id
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def login():
    if rq.method == 'POST':
        existing_user = User.query.filter_by(username=rq.form.get('log_username')).first()
        if existing_user:
            if rq.form.get('log_password') == existing_user.password:
                users = User.query.order_by(User.id).all()
                return rt('users.html', username=existing_user.username, users=users)
            else:
                return  rt('errors.html', error='Wrong password!')
        else:
            return rt('errors.html', error=f'No username "{rq.form.get("log_username")}" found!')
    else:
        return rt('login.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if rq.method == 'POST':
        existing_user = User.query.filter_by(username=rq.form.get('reg_username')).first()
        if existing_user:
            error = f'The username "{rq.form.get("reg_username")}" already exist!'
            return rt('errors.html', error=error)
        elif {rq.form.get("reg_password")} == None:
            return rt('errors.html', error='Password cannot be empty!')
        else:
            new_user = User(username = rq.form.get('reg_username'), password = rq.form.get('reg_password'))
            db.session.add(new_user)
            db.session.commit()
            return rt('login.html')
    else:
        return rt('register.html')
