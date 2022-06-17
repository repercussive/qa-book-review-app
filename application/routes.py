from application import app, db
from application.forms import BookForm, ReviewForm
from application.models import Book, Genre, Review
from application.data import genre_names
from sqlalchemy import desc
from flask import render_template, redirect, url_for, request

@app.before_first_request
def create_tables():
  db.create_all()
  if len(Genre.query.all()) == 0:
    db.session.add_all([Genre(name=name) for name in genre_names])
    db.session.commit()


@app.route('/')
def home():
  recent_reviews = Review.query.order_by(desc(Review.id)).limit(6).all()
  return render_template('index.html', reviews=recent_reviews)


@app.route('/books')
def books():
  title_search_value = request.args.get('title')
  selected_genre_id = request.args.get('genre_id')
  books = Book.query \
              .filter((title_search_value is None) or Book.title.ilike(f'%{title_search_value}%')) \
              .order_by(desc(Book.id)) \
              .all()
  if selected_genre_id:
    selected_genre = Genre.query.get(selected_genre_id)
    books = filter(lambda book: selected_genre in book.genres, books)
    
  return render_template(
    'books.html',
    books_data=generate_books_data(books),
    genres=Genre.query.all(),
    selected_genre_id=selected_genre_id,
    title_search_value=title_search_value,
    str=str
  )


@app.route('/review/<int:id>')
def review(id):
  review = Review.query.get(id)
  return render_template('review.html', review=review)


@app.route('/reviews/<int:book_id>')
def reviews(book_id):
  book = Book.query.get(book_id)
  reviews = Review.query.filter_by(book_id=book_id).all()
  return render_template('review-list.html', book=book, reviews=reviews)


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
  form = BookForm()
  form.genres.choices = get_genre_choices()
  form.submit.label.text = 'Add'

  if form.validate_on_submit():
    new_book = Book(title=form.title.data, author=form.author.data)
    new_book.genres = get_genres_by_ids(form.genres.data or [])
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('add_review', book_id=new_book.id))

  return render_template('book-form.html', form=form, form_action='/add-book')


@app.route('/edit-book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
  book = Book.query.get(id)
  if not book: return redirect(url_for('home'))

  form = BookForm(obj=book)
  form.genres.choices = get_genre_choices()
  form.submit.label.text = 'Save changes'

  if form.validate_on_submit():
    book.title = form.title.data
    book.author = form.author.data
    book.genres = get_genres_by_ids(form.genres.data or [])
    db.session.commit()
    return redirect(url_for('books'))

  form.genres.data = [genre.id for genre in book.genres]
  return render_template('book-form.html', form=form, form_action=f'/edit-book/{id}')


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
        body=form.body.data,
        reviewer_name=form.reviewer_name.data
    )
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('review', id=new_review.id))

  book_id = request.args.get('book_id')
  form.book.data = book_id or 0
  return render_template('review-form.html', form=form, form_action='/add-review', book_id=book_id)


@app.route('/edit-review/<int:id>', methods=['GET', 'POST'])
def edit_review(id):
  review = Review.query.get(id)
  if not review: return redirect(url_for('home'))

  form = ReviewForm(obj=review)
  form.submit.label.text = 'Save changes'
  form.book.choices = [(review.book_id, review.book.title)]

  if form.validate_on_submit():
    review.book_id = form.book.data
    review.rating = form.rating.data
    review.headline = form.headline.data
    review.body = form.body.data
    review.reviewer_name = form.reviewer_name.data
    db.session.commit()
    return redirect(url_for('review', id=review.id))

  return render_template('review-form.html', form=form, form_action=f'/edit-review/{id}')


@app.route('/delete-review/<int:id>', methods=['POST'])
def delete_review(id):
  db.session.delete(Review.query.get(id))
  db.session.commit()
  return redirect(url_for('home'))


# utils

def get_book_choices():
  return [(book.id, book.title) for book in Book.query.all()]

def get_genre_choices():
  return  [(genre.id, genre.name) for genre in Genre.query.all()]

def get_genres_by_ids(genre_ids):
  return [Genre.query.get(genre_id) for genre_id in genre_ids]

def generate_books_data(books):
  books_data = {}
  for book in books:
    ratings = [review.rating for review in Review.query.filter_by(book_id=book.id)]
    num_reviews = len(ratings)
    avg_rating = 0 if num_reviews == 0 else round(sum(ratings) / num_reviews, 1)
    books_data[book.id] = {
      'title': book.title,
      'author': book.author,
      'genres': [genre.name for genre in (book.genres or [])],
      'avg_rating': avg_rating,
      'num_reviews': num_reviews,
      'num_genres': len(book.genres)
    }
  return books_data