from flask import Flask, render_template, url_for, redirect, flash
import requests
import forms
from datetime import datetime

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
    return render_template("book_form.html", form=book_form, action='Add')


@app.route('/form/edit/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    response = requests.get(f'http://localhost:5000/books/{book_id}')
    parsed_json = response.json()['data']
    book_form = forms.BookForm(author=parsed_json['author'], title=parsed_json['title'],
                               description=parsed_json['description'],
                               date=datetime.strptime(parsed_json['date'], '%Y-%m-%d'), image=parsed_json['image'])
    if book_form.validate_on_submit():
        flash(f'{book_form.title.data} has been edited', 'success')
        print(book_form.data)
        requests.put(f'http://localhost:5000/books/{book_id}', book_form.data)
        return redirect(url_for('books_list'))
    return render_template("book_form.html", form=book_form, action='Edit')


if __name__ == '__main__':
    app.run(debug=True)
