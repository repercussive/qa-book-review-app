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
