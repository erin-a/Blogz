from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "runforestrun" 

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner): 
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(60))
    password = db.Column(db.String(16))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'display_entries', 'sign_up_form', 'validate_signup', 'display_usernames']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/')
def display_usernames():
    user_names = User.query.all()
    return render_template('index.html', user_names=user_names)

@app.route('/signup')
def sign_up_form():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    password_verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    password_verify_error = ''
    email_error = ''

    #check for existing name in database
    #username_verify = User.query.filter_by(username=username).first()
    #if not username_verify, do checks - remember to indent and add an else

    if len(username) <= 3 or len(username) >= 20: 
        username_error = "Username must be 3 to 20 characters in length."
    
    if len(password) < 1: 
        password_error = "Please enter a password."
    elif len(password) <= 3 and len(password) >= 20:
        password_error = "Password must be 3 to 20 characters in length."
    
    if password_verify != password:
        password_verify_error = "Passwords do not match."

    if len(email) < 1:
        email_error = "Please enter your email."

    if len(email) > 0:
        if '@' not in email and '.' not in email:
            email_error = "Please enter a valid email."

    if not username_error and not password_error and not password_verify_error and not email_error: 
        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()    
        user_id = new_user.id
        return redirect('/newpost')
    else:
        return render_template('signup.html', username_error=username_error, 
        password_error=password_error, 
        password_verify_error=password_verify_error, 
        email_error=email_error)

@app.route('/valid_sign_up')
def valid_sign_up():
    username = request.args.get('username') 
    return render_template('newpost.html', username=username)

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        password_error = ''
        email_error = ''

        if user and user.password == password:
            if password == user.password:
                session['email'] = email 
                return redirect('/newpost')
            else:
                password_error = "An Incorrect Password was entered, please try again."
                return render_template('login.html')
        else:
            email_error = "No account associated with this email, please sign up."
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/blog')


@app.route('/newpost', methods=['POST', 'GET'])
def create_entry():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        title_error = ''
        body_error = ''

        if len(title) < 1:
            title_error = "Please enter the title."
        
        if len(title) > 120:
            title_error = "Titles must be less than 120 characters long."

        if len(body) < 1:
            body_error = "Body of blog post is required. Because, BLOGZ."

        if len(body) > 5000:
            body_error = "Chatty Kathy, wrap it up under 5000 characters. Please and thank, you."

        if not title_error and not body_error:
            new_entry = Blog(title, body, owner)
            db.session.add(new_entry)
            db.session.commit()    
            blog_id = new_entry.id
            return redirect('/blog?id=' + str(blog_id))
        else:
            return render_template ('newpost.html', title_error=title_error, body_error=body_error)

#create app to display list of all blog entries AND individual entries
@app.route('/blog')
def display_entries():

    #owner = User.query.filter_by(email=session['email']).first()


    #below this displays all entries:
    blog_id = request.args.get('id')
    owner_id = request.args.get('owner_id')
    if (blog_id):
        blog_entry = Blog.query.get(blog_id).first()
        return render_template('singlepost.html', title = "blogz", blog_entry=blog_entry)
    elif (owner_id):
        user_blogs = Blog.query.filter_by(owner_id=owner_id).all()
        return render_template('userposts.html', title="blogz", user_blogs=user_blogs)
    else:
        blog_entries = Blog.query.all()
        return render_template('blog.html', title = "blogz", blog_entries=blog_entries)

  
        # get user_id
        # if there is a user id
            # 


        
        #user_blogs = Blog.query.all(owner=owner).all()
        #return render_template('userposts.html', user_blogs=user_blogs)
    
if __name__ == '__main__':
    app.run()

# fix html for pulling uesr name instead of id number
