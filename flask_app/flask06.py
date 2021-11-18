# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os  # os is used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Note
from models import User
from forms import RegisterForm
from flask import session
import bcrypt
app = Flask(__name__)  # create an app


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page


@app.route('/')
@app.route('/index')
def index():
    a_user = db.session.query(User).filter_by(email='mnaeem1@uncc.edu').one()
    return render_template("index.html", user=a_user)


@app.route('/notes')
def get_notes():
    # retrieve user from database
    # a_user = db.session.query(User).filter_by(email='mnaeem1@uncc.edu').one()
    if session.get('user'):
        # retrieve notes from database
        my_notes = db.session.query(Note).all()

        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/notes/<note_id>')
def get_note(note_id):
    # retrieve user from database
    a_user = db.session.query(User).filter_by(email='mnaeem1@uncc.edu').one()
    # retrieve note from database
    my_notes = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note=my_notes)
    # return "Welcome, Notes App User!"


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    # check method used for request
    if request.method == 'POST':
        #  get title data
        title = request.form['title']
        #  get note data
        text = request.form['noteText']
        note = db.session.query(Note).filter_by(id=note_id).one()
        #  update note data
        note.title = title
        note.text = text
        #  update note in DB
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        # GET request - show new note form to edit note
        # retrieve user from database
        a_user = db.session.query(User).filter_by(email='mnaeem1@uncc.edu').one()
        # retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()

        return render_template('new.html', note=my_note, user=a_user)


@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    # retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    db.session.delete(my_note)
    db.session.commit()

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)

@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    # a_user = {'name': 'Mohammad', 'email': 'mogli@uncc.edu'}
    a_user = db.session.query(User).filter_by(email='mnaeem1@uncc.edu').one()
    # check method used for request
    print('request method is', request.method)
    if request.method == 'POST':
        # get title data
        title = request.form['title']
        # get note data
        text = request.form['noteText']
        # create date stamp
        from datetime import date
        today = date.today()
        # format date mm/dd/yyy
        today = today.strftime("%m-%d-%y")

        new_record = Note(title, text, today)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('get_notes'))
        # request_data = request.form
        # return f"data: {request_data} !"
    else:
        # GET request - show new note form
        # retrieve user from database
        a_user = db.session.query(User).filter_by(email='mnaeem1@uncc.edu').one()
        return render_template('new.html', user=a_user)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'SE3155'

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()  # run under the app context

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
