from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps
import DB
from flask_caching import Cache


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

cache = Cache(app)
notes = DB.notities()
categories = DB.get_categories()
teachers = DB.get_teacher()
gebruikers = DB.adminscherm()

def paginering(page, per_page, notes):
    start = (page-1)*per_page
    end = start +per_page
    return notes[start:end]

#homescreen
@app.before_request
def check_inlog():
    open_routes = ['home', 'static', 'login']
    user = session.get('user')
    
    if not user and request.endpoint not in open_routes:
        return redirect(url_for('login'))
@app.route("/")
@app.route("/home")
def home():
    return render_template('homepage.html')

#login screen
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['teacher_password']

        user = DB.Login(username, password)
        if user:
            session["user"] = user
            print(user)
            return redirect(url_for("display_notes"))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login_page.html', error=error)
    return render_template('login_page.html')

#logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

#delete note
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    if request.method == 'POST':
        if DB.delete(note_id):
            return redirect(url_for('display_notes'))
        else:
            return 'Notities verwijderen mislukt'
    else:
        return redirect(url_for('display_notes'))



#view notes
@app.route("/overzicht", methods=['GET', 'POST'])
@cache.cached(timeout=60)
def display_notes():
    notes = DB.notities()
    page = request.args.get('page', 1, type=int)
    per_page = 4
    total_notes = len(notes)
    paginated_notes = paginering(page, per_page, notes)
    aantal_notities = DB.aantalnotities()
    if not paginated_notes and page != 1:

        return "page not found", 404
    return render_template('overzicht_notities.html', page=page, notes=paginated_notes, total_notes=total_notes, per_page=per_page, aantal_notities=aantal_notities)

#create notes
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        note = request.form['note']
        note_source = request.form['note_source']
        teacher_id = session.get('user')
        category_id = request.form['categorie']


        if DB.create(title, note, note_source, teacher_id,category_id):
            return redirect(url_for('display_notes'))
    categories = DB.get_categories()
    notes = DB.notities()
    teachers = DB.get_teacher()
    return render_template('maaknotitie.html', notes=notes, categories=categories, teachers=teachers)

#edit notes
@app.route('/bewerk')
def edit():
    return render_template('edit_note.html')

@app.route('/delete_user/<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id):
    if request.method == 'POST':
        if DB.delete_gebruiker(teacher_id):
            return redirect(url_for('adminmenu'))
        else:
            return 'Gebruiker verwijderen mislukt'
    else:
        return redirect(url_for('adminpage'))

@app.route('/adminpage/', methods=('GET','POST'))
def adminmenu():
    teacher_id = session.get('user')
    if DB.check_admin(teacher_id) == False:
        return redirect(url_for('display_notes'))
    if request.method == 'POST':
        username = request.form['username']
        teacher_password = request.form['teacher_password']
        display_name = request.form['display_name']
        DB.adminmenu(username, teacher_password, display_name)
    gebruikers = DB.adminscherm()
    return render_template('adminpage.html', gebruikers=gebruikers)

@app.route('/categories/', methods=('GET','POST'))
def categories():
    if request.method == 'POST':
        omschrijving = request.form['omschrijving']
        DB.categoriesaanmaken(omschrijving)
    return render_template('categories.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
