from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = "34asdf98" 

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
    username = db.Column(db.String(60))
    password = db.Column(db.String(16))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, passord, blogs):
        self.username = username
        self.password = password
        self.blogs = blogs



@app.route('/newpost', methods=['POST', 'GET'])
def create_entry():
    # will need to figure out how to incorporate user/owner things
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
            body_error = "Body of blog post is required. Because, Bloggidy."

        if len(body) > 5000:
            body_error = "Chatty Kathy, wrap it up under 5000 characters. Please and thank, you."

        if not title_error and not body_error:
            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.commit()    
            blog_id = new_entry.id
            return redirect('/blog?id=' + str(blog_id))
        else:
            return render_template ('newpost.html', title_error=title_error, body_error=body_error)



#create app to display all blog entries
@app.route('/blog')
def display_entries():
    blog_id = request.args.get('id')
        # ask lucas - why is it: if (blog_id) and not blog_id == True
    if (blog_id):
        blog_entry = Blog.query.get(blog_id)
        return render_template('singlepost.html', title = "Bloggidy", blog_entry=blog_entry)
    else:
        blog_entries = Blog.query.all()
        return render_template('blog.html', title = "Bloggidy", blog_entries=blog_entries)
    
if __name__ == '__main__':
    app.run()


