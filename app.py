from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for flash messages
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
@app.route('/read')
def read():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", post=post)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        
        if not username or not title or not content:
            flash("All fields are required!", "danger")
            return redirect(url_for('add_post'))
        
        new_post = Post(username=username, title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        
        flash("Post added successfully!", "success")
        return redirect(url_for('read'))
    
    return render_template('add_post.html')

if __name__ == '__main__':
    app.run(debug=True)
