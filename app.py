from flask import Flask
app = Flask(__name__)

def getData():
  return 'hello'

@app.route("/")
def index():
    data = getData()
    return data

if __name__ == "__main__":
  app.run()