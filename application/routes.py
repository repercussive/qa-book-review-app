from application import app
from flask import render_template

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
  return 'not yet implemented 🤷‍♂️'