from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

@app.route("/")
@app.route("/home")
def home():
    return render_template('homepage.html')
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login_page.html')
@app.route("/overzicht", methods=['GET','POST'])
def notities():
    return render_template('overzicht_notities.html', messages=messages)

messages = [
            ]

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        vakken = request.form['vakken']
        messages.append({'title': title, 'content': content, 'vakken': vakken})
        return redirect(url_for('notities'))

    return render_template('maaknotitie.html')
@app.route('/bewerk')
def edit():
    return render_template('edit_note.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
