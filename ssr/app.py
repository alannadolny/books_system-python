from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def main():
    response = requests.get('http://localhost:5000/books')
    return render_template("main.html", books=response.json()['data'])


if __name__ == '__main__':
    app.run(debug=True)
