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

    categories_list = list(DB.get_categories())
    return render_template('overzicht_notities.html', page=page, notes=paginated_notes, total_notes=total_notes,
                           per_page=per_page, aantal_notities=aantal_notities, categories_list=categories_list)

@app.route("/search", methods=['POST'])
def search_notes():
    zoekterm = request.form.get('zoekterm', '')
    zoekresultaten = DB.zoek_notities(zoekterm)
    return render_template('overzicht_notities.html', notes=zoekresultaten, zoekterm=zoekterm, page=1, total_notes=len(zoekresultaten), per_page=4, aantal_notities=len(zoekresultaten))

@app.route("/filter_notes", methods=['POST'])
def filter_notes():
    category_omschrijving = request.form.get('category')
    user_filter = request.form.get('user_filter')

    if user_filter == 'current_user':
        user_id = session.get('user')
        filtered_notes = DB.filter_notities_op_gebruiker(user_id, own_notes=True)
    else:
        filtered_notes = DB.filter_notities_op_categorie(
            category_omschrijving) if category_omschrijving else DB.notities()

    categories_list = list(DB.get_categories())
    return render_template('overzicht_notities.html', notes=filtered_notes, page=1, total_notes=len(filtered_notes),
                           per_page=4, aantal_notities=len(filtered_notes), categories_list=categories_list)

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
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = DB.get_note_id(note_id)

    if request.method == 'POST':
        updated_title = request.form['title']
        updated_note = request.form['note']
        updated_note_source = request.form['note_source']
        updated_category_id = request.form['categorie']

        DB.update_note(note_id, updated_title, updated_note, updated_note_source, updated_category_id)
        return redirect(url_for('display_notes'))

    categories = DB.get_categories()
    teachers = DB.get_teacher()
    return render_template('edit_note.html', note=note, categories=categories, teachers=teachers)

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

@app.route('/bewerk_gebruiker/<int:teacher_id>')
def bewerk_gebruiker(teacher_id):
    teacher = DB.get_gebruker_id(teacher_id)
    return render_template('bewerk_gebruiker.html', teacher=teacher)

@app.route('/categories/', methods=('GET','POST'))
def categories():
    if request.method == 'POST':
        omschrijving = request.form['omschrijving']
        DB.categoriesaanmaken(omschrijving)
    return showcategories()

@app.route('/categoriestonen/', methods=('GET', 'POST'))
def showcategories():
    categories_list = DB.categories()
    return render_template('categories.html', categories_list=categories_list)

@app.route('/verwijder_categorie/<int:category_id>', methods=['POST'])
def verwijder_categorie_main(category_id):
    if request.method == 'POST':
        if DB.verwijder_categorie(category_id):
            return redirect(url_for('categories'))
        else:
            return 'Categorie verwijderen mislukt'
    else:
        return redirect(url_for('categories'))

@app.route('/bewerk_categorie_pagina/<int:category_id>')
def bewerk_categorie_pagina(category_id):
    category = DB.get_category_by_id(category_id)
    return render_template('bewerk_categorie.html', category=category)

@app.route('/bewerk_categorie/<int:category_id>', methods=['POST'])
def bewerk_categorie(category_id):
    if request.method == 'POST':
        new_omschrijving = request.form.get('new_omschrijving')
        DB.update_category(category_id, new_omschrijving)

    return redirect(url_for('showcategories'))

if __name__ == "__main__":
    app.debug = True
    app.run()
