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
        password = request.form['password']

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

#view notes
@app.route("/overzicht", methods=['GET', 'POST'])
def display_notes():
    notes = DB.notities()
    page = request.args.get('page', 1, type=int)
    per_page = 2
    total_notes=len(notes)
    paginated_notes = paginering(page, per_page)
    if not paginated_notes and page != 1:
        return "page not found", 404
    return render_template('overzicht_notities.html', page=page ,notes=paginated_notes, total_notes=total_notes, per_page=per_page)

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

ingevulde_formulieren = []

# Variable om de weergave van het formulier te beheren
show_form = False
@app.route('/admin')
def admin():
    return render_template('admin.html', ingevulde_formulieren=ingevulde_formulieren, show_form=show_form)

@app.route('/toon_formulier', methods=['POST'])
def toon_formulier():
    global show_form
    show_form = True
    return redirect('/admin')

@app.route('/formulier', methods=['POST'])
def formulier():
    global show_form
    show_form = False
    naam = request.form['naam']
    leeftijd = request.form['leeftijd']
    ingevulde_formulieren.append({'naam': naam, 'leeftijd': leeftijd})
    return redirect('/admin')



if __name__ == "__main__":
    app.debug = True
    app.run()
