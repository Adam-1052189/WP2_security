from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps
import DB


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

notes = DB.notities()
def paginering(page, per_page):
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
def display_notes():
    notes = DB.notities()
    page = request.args.get('page', 1, type=int)
    per_page = 2
    total_notes=len(notes)
    paginated_notes = paginering(page, per_page)
    aantal_notities = DB.aantalnotities()

    if not paginated_notes and page != 1:
        return "page not found", 404
    return render_template('overzicht_notities.html', page=page ,notes=paginated_notes, total_notes=total_notes, per_page=per_page, aantal_notities=aantal_notities)

#create notes
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        note = request.form['note']
        note_source = request.form['note_source']
        teacher_id = request.form['teacher_id']
        category_id = request.form['category_id']
        notitie = (title, note , note_source , teacher_id , category_id)
        notes.append(notitie)
        if DB.create(title, note, note_source, teacher_id,category_id):
            return redirect(url_for('display_notes'))
    return render_template('maaknotitie.html')

#edit notes
@app.route('/bewerk')
def edit():
    return render_template('edit_note.html')

@app.route('/adminpage/', methods=('GET','POST'))
def adminmenu():
    if request.method == 'POST':
        username = request.form['username']
        teacher_password = request.form['teacher_password']
        display_name = request.form['display_name']
        DB.adminmenu(username, teacher_password, display_name)
    return render_template('adminpage.html')

@app.route('/categories/', methods=('GET','POST'))
def categories():
    if request.method == 'POST':
        omschrijving = request.form['omschrijving']
        DB.categoriesaanmaken(omschrijving)
    return render_template('categories.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
