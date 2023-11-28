from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route('/login')
def home():
    return render_template('homepage.html')
def login():
    return render_template('login_page.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
