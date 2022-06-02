from application import db


class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(60))
  author = db.Column(db.String(40))
  reviews = db.relationship('Review', backref='book')


class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer)
  headline = db.Column(db.String(100))
  body = db.Column(db.String(8000))
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)