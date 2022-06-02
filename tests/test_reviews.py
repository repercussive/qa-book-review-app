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

    # adding book
    self.client.post(
        url_for('add_review'),
        data={
            'book': 1,
            'headline': 'Test Headline',
            'rating': 5,
            'body': 'Test review body'
        }
    )
    test_review = Review.query.first()
    assert test_review.book_id == 1
    assert test_review.headline == 'Test Headline'
    assert test_review.rating == 5
    assert test_review.body == 'Test review body'
