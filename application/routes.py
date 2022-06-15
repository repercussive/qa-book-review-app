from application import app, db
from application.forms import NewBookForm, ReviewForm
from application.models import Book, Review
from sqlalchemy import desc
from flask import render_template, redirect, url_for, request


@app.route('/')
def home():
  recent_reviews = Review.query.order_by(desc(Review.id)).limit(6).all()
  return render_template('index.html', reviews=recent_reviews)


@app.route('/books')
def books():
  all_books = Book.query.order_by(desc(Book.id)).all()
  books_data = {}

  for book in all_books:
    ratings = [review.rating for review in Review.query.filter_by(book_id=book.id)]
    num_reviews = len(ratings)
    avg_rating = 0 if num_reviews == 0 else round(sum(ratings) / num_reviews, 2)
    books_data[book.id] = {
      'title': book.title,
      'author': book.author,
      'avg_rating': avg_rating,
      'num_reviews': num_reviews
    }
    
  return render_template('books.html', books_data=books_data)


@app.route('/review/<int:id>')
def review(id):
  review = Review.query.get(id)
  return render_template('review.html', review=review)


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
  form = NewBookForm()

  if form.validate_on_submit():
    new_book = Book(title=form.title.data, author=form.author.data)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('add_review', book_id=new_book.id))

  return render_template('add-book.html', form=form)


@app.route('/delete-book/<int:id>', methods=['GET', 'POST'])
def delete_book(id):
  book = Book.query.get(id)

  if request.method == 'POST':
    reviews = Review.query.filter_by(book_id=book.id).all()
    for review in reviews: db.session.delete(review)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books'))

  return render_template('delete-book.html', book=book)


@app.route('/add-review', methods=['GET', 'POST'])
def add_review():
  form = ReviewForm()
  form.submit.label.text = 'Add'
  form.book.choices = get_book_choices()

  if form.validate_on_submit():
    new_review = Review(
        book_id=form.book.data,
        rating=form.rating.data,
        headline=form.headline.data,
        body=form.body.data
    )
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('home'))

  form.book.data = 0 if not request.args else (request.args['book_id'] or 0)
  return render_template('review-form.html', form=form, form_action='/add-review')


@app.route('/edit-review/<int:id>', methods=['GET', 'POST'])
def edit_review(id):
  review = Review.query.get(id)
  form = ReviewForm(obj=review)
  form.submit.label.text = 'Save changes'
  form.book.choices = [(review.book_id, review.book.title)]

  if form.validate_on_submit():
    review.book_id = form.book.data
    review.rating = form.rating.data
    review.headline = form.headline.data
    review.body = form.body.data
    db.session.commit()
    return redirect(url_for('home'))

  return render_template('review-form.html', form=form, form_action=f'/edit-review/{id}')


@app.route('/delete-review/<int:id>', methods=['POST'])
def delete_review(id):
  db.session.delete(Review.query.get(id))
  db.session.commit()
  return redirect(url_for('home'))


def get_book_choices():
  return [(book.id, book.title) for book in Book.query.all()]
