from flask_testing import TestCase
from application import app, db


class TestBase(TestCase):
  def create_app(self):
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///",
        SECRET_KEY='TEST_SECRET_KEY',
        DEBUG=True,
        WTF_CSRF_ENABLED=False
    )
    return app

  def setUp(self):
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
