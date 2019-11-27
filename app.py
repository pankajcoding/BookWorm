from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, FileField
from wtforms.validators import InputRequired
from passlib.hash import sha256_crypt
from functools import wraps
import imghdr
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = 'static/img/bookimages/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'bookworm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

#Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('home.html')



# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired(),validators.Length(min=1, max=50)])
    college = StringField('College', [validators.DataRequired(),validators.Length(min=4, max=255)])
    email = StringField('Email', [validators.DataRequired(),validators.Email(),validators.Length(min=5, max=50)])
    phone = StringField('Phone No.', [InputRequired("Please enter your phone no"),validators.Length(min=10, max=10)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        phone=form.phone.data
        college = form.college.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email,phone, college, password) VALUES(%s, %s, %s, %s, %s)", (name, email, phone, college, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            name=data['name']
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email
                session['name']=name
                flash('You are now logged in', 'success')
                return redirect(url_for('buy_books'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/sellbooks')
@is_logged_in
def sellbooks():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cur.execute("SELECT * FROM books WHERE owner = %s", [session['email']])

    books = cur.fetchall()

    if result > 0:
        return render_template('sellbooks.html', books=books)
    else:
        msg = 'No Book has been added'
        return render_template('sellbooks.html', msg=msg)
    # Close connection
    cur.close()

class ImageFileRequired(object):
    """
    Validates that an uploaded file from a flask_wtf FileField is, in fact an
    image.  Better than checking the file extension, examines the header of
    the image using Python's built in imghdr module.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data is None   :
            message = self.message or 'An image file is required'
            raise validators.StopValidation(message)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Book Form Class
class BookForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    subject = StringField('Subject', [validators.Length(min=1, max=200)])
    author = StringField('Author', [validators.Length(min=1, max=200)])
    edition=StringField('Edition', [validators.Length(min=1, max=200)])
    price = StringField('Discounted Price', [validators.Length(min=1, max=200)])
    originalprice=StringField('Original Price', [validators.Length(min=1, max=200)])
    image  = FileField(u'Image File', validators=[])



# Add Book
@app.route('/add_book', methods=['GET', 'POST'])
@is_logged_in
def add_book():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        edition=form.edition.data
        orinigalprice=form.originalprice.data
        price = float(form.price.data)
        subject = form.subject.data
        author=form.author.data
        # if form.image.data:
        #     image_data = request.FILES[form.image.name].read()
        #     open(os.path.join('/data/img', form.image.data), 'w').write(image_data)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        # cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, ))
        cur.execute("INSERT INTO books(title,price, subject,owner,author,originalprice,edition,img) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(title, price,subject,session['email'],author,orinigalprice,edition,filename))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Book Added', 'success')

        return redirect(url_for('sellbooks'))

    return render_template('add_book.html', form=form)


# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_book/<string:id>', methods=['POST'])
@is_logged_in
def delete_book(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM books WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Book Deleted', 'success')

    return redirect(url_for('dashboard'))

@app.route('/buybooks', methods=['GET'])
@is_logged_in
def buy_books():
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM books")

    books = cur.fetchall()
    result = cur.execute("SELECT * FROM subjects")

    subjects = cur.fetchall()


    if result > 0:
        return render_template('buybooks.html', books=books,subjects=subjects)
    else:
        msg = 'No Books Found'
        return render_template('buybooks.html', msg=msg)
    # Close connection
    cur.close()

@app.route('/buybooks/subject/<slug>', methods=['GET'])
@is_logged_in
def buy_books2(slug):
    cur = mysql.connection.cursor()
    # Get article
    subjectresult = cur.execute("SELECT * FROM subjects WHERE slug = %s", [slug])
    subject = cur.fetchone()
    activetab=''
    result=0
    if subjectresult>0:
        activetab=subject['name']
        result = cur.execute("SELECT * FROM books WHERE subject = %s",[subject['name']])
        books = cur.fetchall()
    
    bookresult = cur.execute("SELECT * FROM subjects")
    subjects = cur.fetchall()
    if result > 0:
        return render_template('buybooks.html', books=books,subjects=subjects,activetab=activetab)
    else:
        msg = 'No Books Found'
        return render_template('buybooks.html', msg=msg,subjects=subjects,activetab=activetab)
    # Close connection
    cur.close()
    return slug
@app.route('/getbooks',methods=['GET'])
@is_logged_in
def getbooks():
    cur = mysql.connection.cursor()
    bookresult = cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    return jsonify(books) 




@app.route('/book/<id>',methods=['GET'])
@is_logged_in
def getbook(id):
    cur = mysql.connection.cursor()
    bookresult = cur.execute("SELECT * FROM books WHERE id= %s",[id])
    book = cur.fetchone()
    return render_template('book.html',book=book) 


# User login
@app.route('/buybook', methods=['POST'])
def buyBook():
    # Get Form 
    content = request.json
    book = content['book']
    # owner
    # buyer= session['id']
    # Create cursor
    cur = mysql.connection.cursor()
    #send notification to owner 
    
    #get the owner
    result = cur.execute("SELECT books.*,users.* FROM books  INNER JOIN users ON books.owner=users.email WHERE books.id = %s", [book])

    

    if result > 0:
        # Get stored hash
        data = cur.fetchone()
        # userid = data['id']
        # type="buy"
        # user2=buyer
        # user2name=data['name']
        print('data----',data)
        return jsonify(data)

        



    #send the details of owner to buyer



    # Get user by username



# searchbooks.html
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True,port=5001)
