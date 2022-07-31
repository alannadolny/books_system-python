from flask import Flask, render_template, url_for, redirect, flash, request
import requests
import forms
from datetime import datetime
import filters

app = Flask(__name__)
app.config['SECRET_KEY'] = "219743534356223291801796237134"


@app.route('/')
def books_list():
    response = requests.get('http://api:5000/books')
    filtered_data = filters.get_filtered_data(response.json()['data'],
                                              {'author': request.args.get('author', default=None),
                                               'sortBy': request.args.get('sortBy', default='title'),
                                               'name': request.args.get('name', default=None),
                                               'from': request.args.get('dateFrom', default=None),
                                               'to': request.args.get('dateTo', default=None)})
    filter_form = forms.FiltersForm(author=request.args.get('author', default=None),
                                    sortBy=request.args.get('sortBy', default=None),
                                    name=request.args.get('name', default=''),
                                    dateFrom=filters.return_date(request.args.get('dateFrom', default=None)),
                                    dateTo=filters.return_date(request.args.get('dateTo', default=None)))
    filter_form.author.choices = filters.get_authors(response.json()['data'])
    filter_form.sortBy.choices = [None, 'author', 'title']
    return render_template("main.html", books=filtered_data, form=filter_form)


@app.route('/details/<book_id>')
def book_details(book_id):
    response = requests.get(f'http://api:5000/books/{book_id}')
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
        requests.post('http://api:5000/books', book_form.data)
        return redirect(url_for('books_list'))
    return render_template("book_form.html", form=book_form, action='Add')


@app.route('/form/edit/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    response = requests.get(f'http://api:5000/books/{book_id}')
    parsed_json = response.json()['data']
    book_form = forms.BookForm(author=parsed_json['author'], title=parsed_json['title'],
                               description=parsed_json['description'],
                               date=datetime.strptime(parsed_json['date'], '%Y-%m-%d'), image=parsed_json['image'])
    if book_form.validate_on_submit():
        flash(f'{book_form.title.data} has been edited', 'success')
        print(book_form.data)
        requests.put(f'http://api:5000/books/{book_id}', book_form.data)
        return redirect(url_for('books_list'))
    return render_template("book_form.html", form=book_form, action='Edit')


@app.route('/delete/<book_id>')
def delete_book(book_id):
    requests.delete(f'http://api:5000/books/{book_id}')
    return redirect(url_for('books_list'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
