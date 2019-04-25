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

# instructions says i need separate handler class for each page - but I only have 1...

@app.route('/newpost', methods=['POST', 'GET'])
def verify_entry():
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
            # losing the formatting of the list of existing blogs beneath it
            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.commit()    
            blog_entries = Blog.query.all() 
            return render_template('newpost.html', title = "Bloggidy", blog_entries=blog_entries)
        else:
            # needs to return/redirect the page below, it is not doing this now
            return render_template ('newpost.html', title_error=title_error, body_error=body_error)

    return render_template('newpost.html')


#create app to display all blog entries
@app.route('/blog', methods=['GET', 'POST'])
def display_entries():
    blog_entries = Blog.query.all()
    return render_template('blog.html', title = "Bloggidy", blog_entries=blog_entries)

#for individual blog pages
@app.route('/id', methods=['GET'])
def display_blog():
    title = request.args.get('title')
    return render_template('singlepost.html', title=title)

#    id = request.form['id']
#    title = request.form['title']
#    body = request.form['body']
#    specific_post = Blog(title, body)
#    blog_post = Blog.query.filter(id)
#    return render_template('base.html', title = "Bloggidy", specific_post=specific_post)

if __name__ == '__main__':
    app.run()
