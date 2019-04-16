from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:joseph@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))



    def __init__(self, title, body):
        self.title = title
        self.body = body
        #self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['title']
        new_title = Blog(post_title, post_body)
        db.session.add(new_title)
        db.session.commit()

        post_body = request.form['body']
        new_body = Blog(post_body)
        db.session.add(new_body)
        db.session.commit()

    posts = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", posts=posts)




if __name__ == '__main__':
    app.run()