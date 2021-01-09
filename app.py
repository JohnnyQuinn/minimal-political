from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/")

if __name__ == '__main__':
    app.run(debug=True)
