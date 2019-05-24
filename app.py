from flask import Flask
import requests
import json

app = Flask(__name__)

#######################
# Function to grab the data from the API and return the relevant info
## Params
### None
## Output
#### { string }: JSON object
#######################
def getData():
  url = 'https://api.coinranking.com/v1/public/coin/1/history/30d'
  try:
    response = requests.get(url)
    json = response.json()
    return json['data']['history']
  except requests.exceptions.RequestException as e:
    print(e)

#######################
# Function to return the expected output
## Params
### { string }: data #sorted JSON
## Output
#### { string } JSON obj and result
#######################
def makeJSON(data):


  return jsonObject

# Main and only route in this app. This will also be the homepage
@app.route("/")
def index():
    data = getData()
    sortedData = sorted(data, key=lambda k: k['timestamp'])
    return 'hellio'

if __name__ == "__main__":
  app.run()