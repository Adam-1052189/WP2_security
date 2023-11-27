from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Homepage.html")
@app.route('/login')
def login():
    return render_template('login_page.html')
@app.route("/notes")
def notes():
    return render_template('Overzicht_notities.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
