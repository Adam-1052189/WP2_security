from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

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

messages = [{'title': 'Notitie Naam',
             'content': 'Notitie Inhoud'},
            {'title': 'Notitie Naam',
             'content': 'Notitie Inhoud'}
            ]

@app.route('/create/', methods=('GET', 'POST'))
def create():
    return render_template('maaknotitie.html')
@app.route("/contactformulier", methods=['GET', 'POST'])
def contactformulier():
    return render_template('contactformulier.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
