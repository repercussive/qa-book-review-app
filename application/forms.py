from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, TextAreaField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired, Length, NumberRange


class MultiCheckboxField(SelectMultipleField):
  widget = widgets.ListWidget()
  option_widget = widgets.CheckboxInput()


class BookForm(FlaskForm):
  title = StringField('Title:', validators=[DataRequired(), Length(max=60)])
  author = StringField('Author:', validators=[DataRequired(), Length(max=40)])
  genres = MultiCheckboxField('Genres:', coerce=int)
  submit = SubmitField('[set dynamically]')


class ReviewForm(FlaskForm):
  book = SelectField('Book:', choices=[], validators=[DataRequired()])
  rating = IntegerField('Rating:', default=5, validators=[NumberRange(min=1, max=5)])
  headline = StringField('Review headline:', validators=[DataRequired(), Length(max=100)])
  body = TextAreaField('Write your review here:', validators=[DataRequired(), Length(max=8000)])
  reviewer_name = StringField('Your name (optional)', validators=[Length(max=40)])
  submit = SubmitField('[set dynamically]')
