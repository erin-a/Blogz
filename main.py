from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = "34asdf98" 

# definte table and columns to store blog entries
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name): #will need to add owner inside parenthesis if we reanact that
        self.title = name
        self.posted = False
        #self.owner = owner

#create app for adding an entry to the database
@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_entry = Blog(title, body) 
        db.session.add(new_entry)
        db.session.commit()


    return render_template('newpost.html')

# where do i put form requests    
# where do i put queries?    

#create app to display blog entries
@app.route('/blog', methods=['GET'])
def display_entries():
#    previous_entries = Blog.query.filter_by().all() #what do i filter by

    return render_template('all_posts.html', title=title, body=body)




if __name__ == '__main__':
    app.run()