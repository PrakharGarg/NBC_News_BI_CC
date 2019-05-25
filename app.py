from flask import Flask
import requests
import json
from datetime import datetime

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
  finalData = []
  for object in data:
    newObject = {}
    newObject['date'] = datetime.fromtimestamp(object['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    newObject['price'] = object['price']
    finalData.append(newObject)
  return finalData

# Main and only route in this app. This will also be the homepage
@app.route("/")
def index():
    data = getData()
    # filter the data to only have the first objects of each day
    filteredData = list(filter(lambda d: datetime.fromtimestamp(d['timestamp'] / 1000).strftime('%H:%M:%S') == '00:00:00', data))
    # sort the data into ascending order
    sortedData = sorted(filteredData, key=lambda k: k['timestamp'])
    finalJSON = makeJSON(sortedData)
    print(finalJSON)
    return 'hellio'

if __name__ == "__main__":
  app.run()