from application import db

# association table - allows many-to-many relationship between books & genres
book_genre = db.Table(
    'book_genre',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)


class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(60))
  author = db.Column(db.String(40))
  reviews = db.relationship('Review', backref='book')
  genres = db.relationship('Genre', secondary=book_genre, back_populates='books')


class Genre(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20))
  books = db.relationship('Book', secondary=book_genre, back_populates='genres')


class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer)
  headline = db.Column(db.String(100))
  body = db.Column(db.String(8000))
  reviewer_name = db.Column(db.String(40))
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
