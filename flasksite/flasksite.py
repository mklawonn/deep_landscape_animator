"""
    Small website for hosting the application.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world(name=None):
    return render_template('index.html', gif="static/img/giphy.gif")

@app.route('/animate',methods=["GET","POST"])
def animate(name=None):
    gifLocation = "static/img/giphy.gif"
    return render_template('index.html', gif=gifLocation)

if __name__ == "__main__":
    app.run()
