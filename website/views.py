from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Player
from .import db
import json
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route("/notes", methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the not from HTML
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # Providing the schema for note
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  # Adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/article1')
def article1():
    return render_template("article1.html", user=current_user)


@views.route('/article2')
def article2():
    return render_template("article2.html", user=current_user)


@views.route('/article3')
def article3():
    return render_template("article3.html", user=current_user)


@views.route('/schedule')
def schedule():
    return render_template("schedule.html", user=current_user)


@views.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']

        if len(name) < 1:
            flash('Please enter your name.', category='error')
        elif len(email) < 1:
            flash('Please enter your email.', category='error')
        elif len(position) < 1:
            flash('Please enter your position.', category='error')
        else:
            player = Player(name=name, email=email, position=position)
            db.session.add(player)
            db.session.commit()
            flash('Registration sent!', category='success')

    return render_template('register.html', user=current_user)
