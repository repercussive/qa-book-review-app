from flask import url_for
from application import db
from application.models import Book, Genre, Review
from tests import TestBase


class TestBooks(TestBase):
  # [create] (add-book route, POST) adding a book via POST works
  def test_add_book(self):
    # since the test book has genres associated with it, these need to be in the db first
    test_genres = [Genre(name='Test Genre 1'), Genre(name='Test Genre 2')]
    db.session.add_all(test_genres)
    db.session.commit()
    
    self.client.post(
        url_for('add_book'),
        data={
          'title': 'Test Book',
          'author': 'Test Author',
          'genres': [1, 2]
        }
    )
    
    test_book = Book.query.first()
    assert test_book.title == 'Test Book'
    assert test_book.author == 'Test Author'
    assert test_book.genres == test_genres

  # [read] (books route, GET) receiving books data via GET works
  def test_get_books(self):
    db.session.add(Book(title='A Cool Book', author='A Cool Author'))
    db.session.add(Book(title='A Neat Book', author='A Neat Author'))
    db.session.commit()
    response = self.client.get(url_for('books'))
    assert b'A Cool Book' in response.data
    assert b'A Neat Author' in response.data

  # [update] (edit-book route, POST) editing a book works
  def test_edit_book(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.add(Genre(name='Test Genre'))
    db.session.commit()

    # edit book
    self.client.post(
      url_for('edit_book', id=1),
      data={ 'title': 'Updated Title', 'genres': [1] }
    )

    edited_book = Book.query.get(1)
    assert edited_book.title == 'Updated Title'
    assert edited_book.genres == [Genre.query.get(1)]

  # [delete] (delete-book route, POST) deleting a book works
  def test_delete_book(self):
    book_to_delete = Book(title='Test Book', author='Test Author')
    db.session.add(book_to_delete)
    db.session.commit()

    # associated reviews should also be deleted
    review_to_delete = Review(book_id=book_to_delete.id, headline='', rating=5, body='')
    db.session.add(review_to_delete)
    db.session.commit()

    # delete book
    self.client.post(url_for('delete_book', id=book_to_delete.id))
    assert Book.query.get(book_to_delete.id) is None
    assert Review.query.get(review_to_delete.id) is None

  # (add-book route, GET) add-book route returns a valid response
  def test_add_book_route_get(self):
    response = self.client.get(url_for('add_book'))
    assert response.status_code == 200

  # (edit-book route, GET) edit-book route returns a valid response
  def test_edit_book_route_get(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.commit()
    response = self.client.get(url_for('edit_book', id=1))
    assert response.status_code == 200

  # (delete-book route, GET) delete-book route returns a valid response
  def test_delete_book_route_get(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.commit()
    response = self.client.get(url_for('delete_book', id=1))
    assert response.status_code == 200 
