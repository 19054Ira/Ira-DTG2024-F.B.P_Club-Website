from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .import db
import json
views = Blueprint('views', __name__)
 
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/notes", methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        note = request.form.get('note') #Gets the not from HTML
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id) #Providing the schema for note
            db.session.add(new_note) #Adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')
      
    return render_template("notes.html",user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
    

