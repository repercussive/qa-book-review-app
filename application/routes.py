from application import app, db
from application.forms import NewBookForm, NewReviewForm
from application.models import Book, Review
from flask import render_template, redirect, url_for


@app.route('/')
def home():
  recent_reviews = Review.query.limit(6).all()
  return render_template('index.html', reviews=recent_reviews)

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
 

@app.route('/add-review', methods=['GET', 'POST'])
def add_review(): 
  form = NewReviewForm()
  books = Book.query.all()
  
  for book in books:
    form.book.choices.append([book.id, f'{book.title} ({book.author})'])  # type: ignore

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

  return render_template('add-review.html', form=form)


@app.route('/delete-review/<int:id>', methods=['POST'])
def delete_review(id):
  db.session.delete(Review.query.get(id))
  db.session.commit()
  return redirect(url_for('home'))