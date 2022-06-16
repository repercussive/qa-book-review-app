from application import db
from application.models import Genre

genre_names = [
  'action',
  'mystery',
  'fantasy',
  'sci-fi',
  'historical fiction',
  'romance',
  'thriller',
  'non-fiction'
]

db.drop_all()
db.create_all()
db.session.add_all([Genre(name=name) for name in genre_names])
db.session.commit()
