from application import app, db
from application.forms import NewBookForm
from application.models import Book
from flask import render_template, redirect, url_for


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
  form = NewBookForm()

  if form.validate_on_submit():
    new_book = Book(title=form.title.data, author=form.author.data)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('home'))

  return render_template('add-book.html', form=form)
