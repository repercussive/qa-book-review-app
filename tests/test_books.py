from flask import url_for
from application import db
from application.models import Book, Review
from tests import TestBase


class TestBooks(TestBase):
  # [create] (add-book route, POST) adding a book via POST works
  def test_add_book(self):
    self.client.post(
        url_for('add_book'),
        data={'title': 'Test Book', 'author': 'Test Author'}
    )
    test_book = Book.query.first()
    assert test_book.title == 'Test Book'
    assert test_book.author == 'Test Author'

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
    book_to_edit = Book(title='Test Book', author='Test Author')
    db.session.add(book_to_edit)
    db.session.commit()

    # edit book
    self.client.post(
      url_for('edit_book', id=book_to_edit.id),
      data={ 'title': 'Updated Title' }
    )
    assert Book.query.get(book_to_edit.id).title == 'Updated Title'

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
