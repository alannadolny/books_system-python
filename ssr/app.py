from flask import Flask, render_template, url_for, redirect, flash
import requests
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = "219743534356223291801796237134"


@app.route('/')
def books_list():
    response = requests.get('http://localhost:5000/books')
    return render_template("main.html", books=response.json()['data'])


@app.route('/details/<book_id>')
def book_details(book_id):
    response = requests.get(f'http://localhost:5000/books/{book_id}')
    parsed_json = response.json()['data']
    to_return = render_template("book_details.html",
                                book=parsed_json) if parsed_json != 'not found' else render_template(
        "not_found.html")
    return to_return


@app.route('/form/add', methods=['GET', 'POST'])
def create_book():
    book_form = forms.BookForm()
    if book_form.validate_on_submit():
        flash('Book added', 'success')
        requests.post('http://localhost:5000/books', book_form.data)
        return redirect(url_for('books_list'))
    return render_template("book_form.html", form=book_form)


if __name__ == '__main__':
    app.run(debug=True)
