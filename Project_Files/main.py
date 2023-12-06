from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
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

@app.route("/notitie")
def notitieaanmaken():
    return render_template('maaknotitie.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
