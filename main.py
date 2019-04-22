from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "34asdf98" 


# definte table and columns to store blog entries
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner




#class User(db.Model):

#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(120), unique=True)
#    password = db.Column(db.String(120))
#    title = db.relationship('Title', backref='owner')

#    def __init__(self, email, password):
#        self.email = email
#        self.password = password



#create app for adding an entry to the database
@app.route('/', methods=['GET', 'POST'])
def add_entry:

#create app to display blog entries
@app.route('/', methods=['GET'])






# app that checks if you're logged in already
#@app.before_request 
#def require_login():
#    allowed_routes = ['login', 'register'] 
##    if request.endpoint not in allowed_routes and 'email' not in session:
#        return redirect('/login')

#@app.route('/login', methods=["POST", "GET"])
#def login():
#    if request.method == 'POST':
#        email = request.form['email']
#        password = request.form['password']
#        user = User.query.filter_by(email=email).first()
#        if user and user.password == password:
#            session['email'] = email 
#            flash("Logged in")
#            return redirect('/')
#        else:
#            flash('User password incorrect, or user does not exist', 'error')

#    return render_template('login.html')

#@app.route('/register', methods=["POST", "GET"])
#def register():
#    if request.method == 'POST':
#        email = request.form['email']
#        password = request.form['password']
#        verify = request.form['verify']

        # to do  - use validation from user-signup to set up validation

#        existing_user = User.query.filter_by(email=email).first()
#        if not existing_user:
#            new_user = User(email, password)
#            db.session.add(new_user)
#            db.session.commit()
#            session['email'] = email 
#            return redirect('/')
#        else:
#            # to do - user better reponse msg
#            return '<h1>Duplicate user</h1>'

#    return render_template('register.html')

#@app.route('/logout')
#def logout():
#    del session['email']
#    return redirect('/')

if __name__ == '__main__':
    app.run()