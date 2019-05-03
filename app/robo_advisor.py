
# Robo Advisor and Portfolio Manager
### Created 2/25/2019 by Kuran P. Malhotra
### Starter Repo from https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/projects/robo-advisor.md

import datetime as dt
from dotenv import load_dotenv
import json
import os
import pandas as pd
import requests
import statistics as stat

from functions import *


load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
# print("API KEY: " + api_key)

line = "=" * 50
# global symbol
# symbol = ""
# stock_class = ""
# index_ticker = ""
# settings_binary = int(0)


print(line)
print("")
print("Welcome to the Robo Advisor Portfolio Manager.")
print("")
print(line)
getsymbol()
define_stock()
print(line)

# see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
# Assemble URL

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}"
# print(request_url)

# TODO: use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...

response = requests.get(request_url)

# Validate a valid response given improper response codes:

if "Error" in response.text:
	print("Hmm. Something went wrong there...try again later!")
	exit()

# print("RESPONSE STATUS: " + str(response.status_code))
# print("RESPONSE TEXT: " + response.text)

# Turn JSON into readable format:

parsed_response = response.json()

time = []
open_price = []
high_price = []
low_price = []
close_price = []
volume = []

# Got some help from Hiep here:

for k, v in parsed_response['Time Series (Daily)'].items():
	time.append(k)
	open_price.append(float(v['1. open']))
	high_price.append(float(v['2. high']))
	low_price.append(float(v['3. low']))
	close_price.append(float(v['4. close']))
	volume.append(v['5. volume'])

# print(time, open_price, high_price, low_price, close_price, volume)

# TODO: further parse the JSON response...

# Make the json easier via a data frame:

data = pd.DataFrame({
	'Time':time,
	'Opening Price': open_price,
	'High Price': high_price,
	'Low Price': low_price,
	'Closing Price': close_price,
	'Volume': volume
	})

# TODO: traverse the nested response data structure to find the latest closing price and other values of interest...

latest_price_usd = "$" + "{0:,.2f}".format(float(data.iloc[0]['Closing Price'])) #<—— Taken from Groceries Exercise

#Parse latest date, taken from exec dashboard:
latest_time = time[0]
f = list(latest_time.upper())
year = f[0] + f[1] + f[2] + f[3]
year = (int(year))
monthnum = f[5] + f[6]
day = f[8] + f[9]
day = int(day)
monthnum = (int(monthnum))
latest_month_name = convert_month(monthnum)

# Get current time (Help from: https://docs.python.org/2/library/datetime.html):
now = dt.datetime.now()
cyear = now.year
cmonth = int(now.month)
cmonth_name = convert_month(cmonth)
cday = now.day
ctime = dt.datetime.time(dt.datetime.now())
ctime = ctime.strftime("%I:%M%P")

# Get the 100-day high and low prices:
timehigh = float(max(high_price))
timehigh = "$" + "{0:,.2f}".format(timehigh)

timelow = float(min(low_price))
timelow = "$" + "{0:,.2f}".format(timelow)

# Save data to CSV, with help from class notes + Matt + this site: https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
cwd = os.getcwd()
lencwd = len(cwd)
pathlen = lencwd
path = cwd[0:pathlen] + "/data/"

data.to_csv(path + str(cyear) + "-" + str("{0:02d}".format(cmonth)) + " " + symbol + ".csv")

# Pull market data based on stock market capitalization: 

index_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={index_ticker}&outputsize=compact&apikey={api_key}"
index_response = requests.get(index_url)

# Validate index selections from settings function + ensure proper data: 

if "Error" in index_response.text:
	large_cap_index = "SPY"
	mid_cap_index = "RMCCX"
	small_cap_index = "^RUT"
	print("We ran into an error with your benchmark and unfortunately had to utilize the default benchmarks. Please redefine your stock.")
	define_stock()
	index_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={index_ticker}&outputsize=compact&apikey={api_key}"
	index_response = requests.get(index_url)

# Read index data into lists: 

parsed_index_data = index_response.json()

index_time = []
index_open_price = []
index_high_price = []
index_low_price = []
index_close_price = []
index_volume = []

for k, v in parsed_index_data['Time Series (Daily)'].items():
	index_time.append(k)
	index_open_price.append(float(v['1. open']))
	index_high_price.append(float(v['2. high']))
	index_low_price.append(float(v['3. low']))
	index_close_price.append(float(v['4. close']))
	index_volume.append(v['5. volume'])

# Benchmark calculations: 

index_daily_delta = []

for n in range(0,len(index_close_price)-1):
	index_daily_delta.append((index_close_price[n]-index_close_price[n+1])/(index_close_price[n+1]))

index_sigma = stat.stdev(index_daily_delta)
index_xbar = stat.mean(index_daily_delta)
index_coeff = index_sigma/index_xbar
index_sharpe = index_xbar / index_sigma
index_sharpe_str = str("{0:,.2f}".format(index_sharpe))


# Stock Calculations:

daily_delta = []

for n in range(0,len(close_price)-1):
	daily_delta.append((close_price[n]-close_price[n+1])/(close_price[n+1]))

sigma = stat.stdev(daily_delta)
xbar = stat.mean(daily_delta)
coeff = sigma/xbar
sharpe = xbar / sigma
sharpe_str = str("{0:,.2f}".format(sharpe))

# Recommendation Engine:

if sharpe > index_sharpe:
	rec_sum = "Buy!"
	rec_exp = f"The Sharpe ratio of {symbol} is greater than the Sharpe ratio of the benchmark {index_ticker}." 
	rec_exp2 = f"This means that you can gain equivalent returns with less risk by investing in {symbol}."
elif sharpe < index_sharpe:
	rec_sum = "Sell!"
	rec_exp = f"The Sharpe ratio of {symbol} is less than the Sharpe ratio of the benchmark {index_ticker}." 
	rec_exp2 = f"This means that you can gain equivalent returns with less risk by investing in {index_ticker}."
elif sharpe == index_sharpe:
	rec_sum = "Hold!"
	rec_exp = f"The Sharpe ratio of {symbol} is equal to the Sharpe ratio of the benchmark {index_ticker}." 
	rec_exp2 = f"This means that you can gain equivalent returns with equivalent risk by investing in either."

# Final Outputs:

print(line)
print(f"STOCK SYMBOL: {symbol}")
print(f"BENCHMARKED AGAINST: {index_ticker.upper()}")
print(f"RUN AT: {ctime} on {cmonth_name} {cday}, {cyear}")
print(line)
print(f"LATEST DAY OF AVAILABLE DATA: {latest_month_name} {day}, {year}")
print(f"LATEST DAILY CLOSING PRICE: {latest_price_usd}")
print(f"100 DAY HIGH: {timehigh}")
print(f"100 DAY LOW: {timelow}")
print(line)
print(f"RECOMMENDATION: {rec_sum}")
print(f"RECOMMENDATION REASON: {rec_exp}")
print(f"RECOMMENDATION EXPLANATION: {rec_exp2}")
print(line)
