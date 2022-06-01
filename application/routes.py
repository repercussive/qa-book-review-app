from application import app

@app.route('/')
def home():
  return "There's nothing here yet!"