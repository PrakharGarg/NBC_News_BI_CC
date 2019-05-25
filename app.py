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
# Function to return the direction, price, and change
## Params
### { obj }: current day object
### { float }: price of last known day
## Output
#### { string, Float, string } direction, price, change
#######################
def getDirectionChange(object, lastPrice):
  currentPrice = float(object['price'])
  if (lastPrice == 'na'):
    return 'na', currentPrice, 'na'

  change = currentPrice - lastPrice
  if (currentPrice > lastPrice):
    return ('up', currentPrice, change)
  if (currentPrice < lastPrice):
    return ('down', currentPrice, change)
  else:
    return ('same', currentPrice, 0)

#######################
# Function to return the formatted date and weekday
## Params
### { string }: timestamp
## Output
#### { string, string }: formatted date, weekday
#######################
def getDate(timestamp):
  days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
  weekdayInt = datetime.fromtimestamp(timestamp / 1000).weekday()
  weekday = days[weekdayInt]

  return (date,weekday)


#######################
# Function to return the expected output
## Params
### { string }: data #sorted and filtered JSON
## Output
#### { string } JSON obj and result
#######################
def makeJSON(data):
  finalData = []
  lastPrice = 'na'
  low = 0
  high = 0
  # iterate through all days and build its data
  for object in data:
    change = 0
    newObject = {}
    lowSinceStart = False
    highSinceStart = False

    date, day = getDate(object['timestamp'])

    newObject['date'] = date
    newObject['price'] = float(object['price'])

    direction, currentPrice, change = getDirectionChange(object, lastPrice)
    newObject['direction'] = direction
    newObject['change'] = change

    newObject['dayOfWeek'] = day
    # on the first day set the low and high to its value
    if (low == 0):
      high = currentPrice
      low = currentPrice
      lowSinceStart = True
      highSinceStart = True
    elif (currentPrice > high):
      high = currentPrice
      highSinceStart = True
    elif (currentPrice < low):
      low = currentPrice
      lowSinceStart = True

    newObject['highSinceStart'] = highSinceStart
    newObject['lowSinceStart'] = lowSinceStart

    lastPrice = currentPrice
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