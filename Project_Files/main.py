from flask import Flask, render_template, redirect, url_for, request, flash
import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

@app.route("/")
@app.route("/home")
def home():
    return render_template('homepage.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if DB.login(username, password):
            return redirect('/overzicht')
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login_page.html', error=error)
    return render_template('login_page.html')

@app.route("/overzicht", methods=['GET', 'POST'])
def notities():
    return render_template('overzicht_notities.html', messages=messages)

messages=[
            ]
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        note = request.form['note']

        if DB.create(title, note):
            return redirect(url_for('notities'))
    return render_template('maaknotitie.html')
@app.route('/bewerk')
def edit():
    return render_template('edit_note.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
