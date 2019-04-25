from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = "34asdf98" 

# definte table and columns to store blog entries
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body): #will need to add owner inside parentheses if we reanact that
        self.title = title
        self.body = body #if this is supposed to be unique, wouldn't the id be better to use here? do i need to require the blog titles to be unique?
        #self.owner = owner

# instrustions says i need separate handler class for each page - but I only have 1...

#create app for adding an entry to the database
@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_entry = Blog(title, body)
        db.session.add(new_entry)
        db.session.commit()

    blog_entries = Blog.query.all()

    return render_template('newpost.html', blog_entries=blog_entries)

# where do i put form requests    
# where do i put queries?    

#create app to display blog entries
@app.route('/all', methods=['GET'])
def display_entries():
    #Blogs = Blog.query.filter_by().all() #what do i filter by
    blog_entries = Blog.query.all()
    return render_template('allposts.html', title = "Bloggidy", blog_entries=blog_entries)

#@app.route('/blog', methods=['GET'])
#def display_entries():


if __name__ == '__main__':
    app.run()