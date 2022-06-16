from application import db
from application.models import Book, Review
from flask import url_for
from tests import TestBase


class TestReviews(TestBase):
  # (add-review route, POST) adding a review via POST works
  def test_add_review(self):
    # the review's book_id must refer to a real book, so we have to add one first
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.commit()

    # add review
    self.client.post(
        url_for('add_review'),
        data={
            'book': 1,
            'headline': 'Test Headline',
            'rating': 5,
            'body': 'Test review body',
            'reviewer_name': 'Bob'
        }
    )
    test_review = Review.query.first()
    assert test_review.book_id == 1
    assert test_review.headline == 'Test Headline'
    assert test_review.rating == 5
    assert test_review.body == 'Test review body'
    assert test_review.reviewer_name == 'Bob'

  # (index route, GET) basic data for recent reviews is included in homepage
  def test_get_recent_reviews(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.add(Review(book_id=1, headline='Test Headline', rating=5, body='Test review body'))
    db.session.commit()

    response = self.client.get(url_for('home'))
    assert b'Test Headline' in response.data

  # (review route, GET) getting a single review works
  def test_get_review_by_id(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.add(Review(book_id=1, headline='Test Headline', rating=5, body='Test review body'))
    db.session.commit()

    response = self.client.get(url_for('review', id=1))
    assert b'Test Headline' in response.data
    assert b'Test review body' in response.data

  # (reviews route, GET) getting reviews for a specific book works
  def test_get_reviews_by_book(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.add(Review(book_id=1, headline='Test Headline 1', rating=5, body='Test review body'))
    db.session.add(Review(book_id=1, headline='Test Headline 2', rating=5, body='Test review body'))
    db.session.commit()

    response = self.client.get(url_for('reviews', book_id=1))
    assert b'Test Headline 1' in response.data
    assert b'Test Headline 2' in response.data

  # (edit-review route, POST) editing a review works
  def test_edit_review(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    review_to_edit = Review(book_id=1, headline='Test Headline', rating=5, body='Test review body')
    db.session.add(review_to_edit)
    db.session.commit()

    # edit review headline
    self.client.post(
        url_for('edit_review', id=review_to_edit.id),
        data={
            'book': 1,
            'headline': 'Updated Headline',
            'rating': 5,
            'body': 'Test review body'
        }
    )
    test_review = Review.query.get(review_to_edit.id)
    assert test_review.headline == 'Updated Headline'

  # (delete-review route, POST) deleting a review via POST works
  def test_delete_review(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    review_to_delete = Review(book_id=1, headline='Test Headline', rating=5, body='Test review body')
    db.session.add(review_to_delete)
    db.session.commit()

    # delete review
    self.client.post(url_for('delete_review', id=review_to_delete.id))

    # it's gone
    assert Review.query.get(review_to_delete.id) is None

  # (add-review route, GET) add-review route returns a valid reponse
  def test_add_review_route_get(self):
    response = self.client.get(url_for('add_review'))
    assert response.status_code == 200

  # (edit-review route, GET) edit-review route returns a valid reponse
  def test_edit_review_route_get(self):
    db.session.add(Book(title='Test Book', author='Test Author'))
    db.session.add(Review(book_id=1, headline='Test Headline', rating=5, body='Test review body'))
    response = self.client.get(url_for('edit_review', id=1))
    assert response.status_code == 200
