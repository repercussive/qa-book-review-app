from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class NewBookForm(FlaskForm):
  title = StringField('Title:', validators=[DataRequired(), Length(max=60)])
  author = StringField('Author:', validators=[DataRequired(), Length(max=40)])
  submit = SubmitField('Add')


class ReviewForm(FlaskForm):
  book = SelectField('Book:', choices=[], validators=[DataRequired()])
  rating = IntegerField('Rating:', default=5, validators=[NumberRange(min=1, max=5)])
  headline = StringField('Review headline:', validators=[DataRequired(), Length(max=100)])
  body = TextAreaField('Write your review here:', validators=[DataRequired(), Length(max=8000)])
  submit = SubmitField('Add')
  