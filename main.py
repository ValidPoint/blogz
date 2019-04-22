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

@app.route('/')
def index():
    return redirect('/blog')


@app.route('/blog', methods=['POST', 'GET'])
def get_post():

    #if request.method == 'POST':
        #post_title = request.form['title']
        #post_body = request.form['body']
        #new_blog = Blog(post_title, post_body)
        #db.session.add(new_blog)
        #db.session.commit()


    

    #post_id = ''
    #post_ids = request.args.get('id')
    #if post_ids == '':
        #posts = Blog.query.all()
        #return render_template('blog2.html', title=Build_A_Blog, posts=posts)
    #else:
        #return render_template('blog3.html', post_ids=post_ids)


    post_id = request.args.get('id')
    if (post_id):
        post = Blog.query.get(post_id)
        return render_template('blog3.html', post=post)
    else:
        posts = Blog.query.all()
        return render_template('blog2.html', posts=posts)


#@app.route('/delete-blog', methods=['POST'])
#def hub():

    #post_id = int(request.form['post-id'])
    #post = Blog.query.get(post_id)
    #post.completed = True
    #db.session.add(post)
    #db.session.commit()

    #return redirect('/blog')

@app.route('/newpost')
def post():
    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def make_post():

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        new_blog = Blog(post_title, post_body)
        db.session.add(new_blog)
        db.session.commit()

        url = "/blog?id=" + str(new_blog.id)
        return redirect(url)


@app.route('/newpost', methods=['POST'])
def user_post():

    title = request.form['title']
    body = request.form['body']

    title_error = ''
    body_error = ''

    if len(title) == 0:
        title_error = 'No Text Found'

    if len(body) == 0:
        body_error = 'No Text Found'

    if not title_error and not body_error:
        title = request.form['title']
        body = request.form['body']
        return render_template('blog2.html')
    else:
        return render_template('blog.html', title_error=title_error, body_error=body_error, title=title, body=body)

#@app.route('/newpost', methods=['POST', 'GET'])
#def make_post():

     #if request.method == 'POST':
        #post_title = request.form['title']
        #post_body = request.form['body']
        #new_blog = Blog(post_title, post_body)
        #db.session.add(new_blog)
        #db.session.commit()


     #posts = Blog.query.all()
     #return render_template('blog2.html',title="Build A Blog", posts=posts)






if __name__ == '__main__':
    app.run()