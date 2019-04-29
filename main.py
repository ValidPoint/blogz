from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:chico@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "#Secretkey"


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))



    def __init__(self, title, body, username):
        self.title = title
        self.body = body
        self.owner = username
        #self.completed = False


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')


    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'get_post', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        #user2 = User.query.filter_by(password=password).first()
        
        username_error = ''
        password_error = ''

        if username != User.username:
            username_error = 'Username Does Not Exist'

        if password != User.password:
            password_error = 'Password is Incorrect'
        
        if not username_error and not password_error:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('login.html', username_error=username_error, password_error=password_error, username=username, password=password)
    
    
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        #existing_user = User.query.filter_by(username=username).first()
        
        username_error = ''
        password_error = ''

        if len(username) == 0:
            username_error = 'One Or More Fields Are Invalid'

        if len(username) < 3:
            username_error = 'Username is Invalid'

        #if username in existing_user:
            #username_error = 'Username Already Exists'

        if len(password) == 0:
            password_error = 'One Or More Fields Are Invalid'

        if len(password) < 3:
            password_error = 'Password is Invalid'

        if password != verify:
            password_error = 'Passwords Do Not Match'

        if not username_error and not password_error:
            username = request.form['username']
            password = request.form['password']
            verify = request.form['verify']
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/blog')
        else:
            username_error = 'Username is Invalid'
            return render_template('signup.html', username_error=username_error, password_error=password_error, username=username, password=password, verify=verify)


    return render_template('signup.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/blog')



@app.route('/', methods=['POST', 'GET'])
def index():
    user = User.query.all()
    return render_template('index.html', users=user)
    #return "<p>"+str(user)+"</p>"


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

    user_id = request.args.get('user')
    post_id = request.args.get('id')
    if (user_id):
        blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('blog4.html', blogs=blogs)
    elif (post_id):
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('blog3.html', post=post, user=post.owner.username)
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

    username = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        post_title = request.form['title']
        post_body = request.form['body']
        #post_username = request.form['username']
        #new_blog = Blog(post_title, post_body)
        #db.session.add(new_blog)
        #db.session.commit()

        #url = "/blog?id=" + str(new_blog.id)
        #return redirect("/blog")


#@app.route('/newpost', methods=['POST'])
#def user_post():

    #title = request.form['title']
    #body = request.form['body']

    title_error = ''
    body_error = ''

    if len(post_title) == 0:
        title_error = 'No Text Found'

    if len(post_body) == 0:
        body_error = 'No Text Found'

    if not title_error and not body_error:
        post_title = request.form['title']
        post_body = request.form['body']
        #post_username = request.form['username']
        new_blog = Blog(post_title, post_body, username)
        db.session.add(new_blog)
        db.session.commit()
        url = "/blog?id=" + str(new_blog.id)
        #return render_template('blog2.html')
        return redirect(url)
    else:
        return render_template('blog.html', title_error=title_error, body_error=body_error, post_title=post_title, post_body=post_body)

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