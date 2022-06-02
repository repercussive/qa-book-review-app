from re import L
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NewBookForm(FlaskForm):
  title = StringField('Title:', validators=[DataRequired(), Length(max=60)])
  author = StringField('Author:', validators=[DataRequired(), Length(max=40)])
  submit = SubmitField('Add')
