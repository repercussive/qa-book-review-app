from flask import url_for
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
