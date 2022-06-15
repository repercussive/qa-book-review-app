from flask import url_for
from application import db
from application.models import Book
from tests import TestBase


class TestBooks(TestBase):
  # (add-book route, POST) adding a book via POST works
  def test_add_book(self):
    self.client.post(
        url_for('add_book'),
        data={'title': 'Test Book', 'author': 'Test Author'}
    )
    test_book = Book.query.first()
    assert test_book.title == 'Test Book'
    assert test_book.author == 'Test Author'

  # (books route, GET) receiving books data via GET works
  def test_get_books(self):
    db.session.add(Book(title='A Cool Book', author='A Cool Author'))
    db.session.add(Book(title='A Neat Book', author='A Neat Author'))
    db.session.commit()
    response = self.client.get(url_for('books'))
    assert b'A Cool Book' in response.data
    assert b'A Neat Author' in response.data
