
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


load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
# print("API KEY: " + api_key)

line = "=" * 50
global symbol
symbol = ""
stock_class = ""
index_ticker = ""
settings_binary = int(0)

def settings(): # Functionality to change index benchmarks
	global large_cap_index
	global mid_cap_index
	global small_cap_index
	global settings_binary
	settings_binary = int(1)
	large_cap_index = "SPY"
	mid_cap_index = "RMCCX"
	small_cap_index = "^RUT"
	print(line)
	print("")
	print("Here, you can choose which benchmarks you wish to use.")
	print(f"    DEFAULTS: Large Cap: {large_cap_index}, Mid Cap: {mid_cap_index}, Small Cap: {small_cap_index}")
	print("")
	print(line)
	large_cap_index = ""
	mid_cap_index = ""
	small_cap_index = ""
	settings_selection = input("Choose '1' to edit the Large Cap benchmark, '2' for the Mid Cap, and '3' for the Small Cap. Choose '0' to return to the defaults: ")
	settings_selection = int(settings_selection)
	if settings_selection == 0:
		large_cap_index = "SPY"
		mid_cap_index = "RMCCX"
		small_cap_index = "^RUT"
	elif settings_selection == 1:
		large_cap_index = input("Please input a valid Large Cap index's ticker symbol: ")
		mid_cap_index = "RMCCX"
		small_cap_index = ""
		print(f"Setting saved: {large_cap_index} is the new Large Cap benchmark")
	elif settings_selection == 2:
		large_cap_index = "SPY"
		mid_cap_index = input("Please input a valid Mid Cap index's ticker symbol: ")
		small_cap_index = ""
		print(f"Setting saved: {mid_cap_index} is the new Mid Cap benchmark")
	elif settings_selection == 3:
		large_cap_index = "SPY"
		mid_cap_index = "RMCCX"
		small_cap_index = input("Please input a valid Small Cap index's ticker symbol: ")
		print(f"Setting saved: {small_cap_index} is the new Small Cap benchmark")
	else:
		print("Please choose a valid settings selection.")
		settings()

def getsymbol(): # function to include validation into the system.
	global large_cap_index
	global mid_cap_index
	global small_cap_index
	global settings_binary
	global symbol
	symbol = input("Please specify a stock symbol ('settings' for settings or 'exit' to exit): ") 
	if symbol == "exit":
		exit()
	if symbol == "settings":
		settings()
		settings_binary = 1
		getsymbol()
	if len(symbol) < 1:
		print("Oops, we didn't get your symbol. Mind trying again?")
		getsymbol() 
	elif len(symbol) > 6: # Per a quick Google, 6 seems to be the max length of a ticker: https://www.quora.com/Whats-the-shortest-and-the-longest-that-a-companys-ticker-can-be-on-a-stock-market-exchange
		print("Hmm...that symbol seems a bit long...mind trying again?")
		getsymbol()
	
	if settings_binary == int(0): 
		large_cap_index = "SPY"
		mid_cap_index = "RMCCX"
		small_cap_index = "^RUT"
	
	symbol = symbol.upper()

def define_stock(): # get more information about the stock to determine appropriate index bechmark
	global stock_class
	global index_ticker
	stock_class = int(input("Describe the stock's market capitalization (1=Large Cap, 2=Mid Cap, 3=Small Cap): "))
	if stock_class not in [1,2,3]:
		print("Hmm...we couldn't understand that, please try again.")
		define_stock()
	if stock_class == 1: 
		index_ticker = large_cap_index
	elif stock_class == 2:
		index_ticker = mid_cap_index
	elif stock_class == 3:
		index_ticker = small_cap_index
	print("Thanks! Let's see what we can find...")

def convert_month(month_num): # convert month number to name
	global month_name
	if month_num == 1:
		month_name = "January"
	elif month_num == 2:
		month_name = "February"
	elif month_num == 3:
		month_name = "March"
	elif month_num == 4:
		month_name = "April"
	elif month_num == 5:
		month_name = "May"
	elif month_num == 6:
		month_name = "June"
	elif month_num == 7:
		month_name = "July"
	elif month_num == 8:
		month_name = "August"
	elif month_num == 9:
		month_name = "September"
	elif month_num == 10:
		month_name = "October"
	elif month_num == 11:
		month_name = "November"
	elif month_num == 12:
		month_name = "December"
	return month_name

def to_usd(amount): # convert value to $00.00 format
    two_decimal = "{0:.2f}".format(amount)
    dollar_str = f'${two_decimal}'
    return dollar_str

def compile_url(ticker,key): # create alphavantage URL with specified ticker and key
	url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={key}"
	return url

def validate_response(response): # validate a good API call (no errors)
	if "Error" in response:
		print("Hmm. Something went wrong there...try again later!")
		return "Error"
	else: return "Good"

def write_to_csv(dataset): # Save data to CSV, with help from class notes + Matt + this site: https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
	cwd = os.getcwd()
	lencwd = len(cwd)
	pathlen = lencwd
	global path
	path = cwd[0:pathlen] + "/data/"
	dataset.to_csv(path + str(cyear) + "-" + str("{0:02d}".format(cmonth)) + " " + symbol + ".csv")

if __name__ == '__main__':

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

	request_url = compile_url(symbol, api_key)

	response = requests.get(request_url)
	response_val = response.text
	if validate_response(response_val) == "Error":
		exit()

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

	# Make the json easier via a data frame:

	data = pd.DataFrame({
		'Time':time,
		'Opening Price': open_price,
		'High Price': high_price,
		'Low Price': low_price,
		'Closing Price': close_price,
		'Volume': volume
		})

	latest_price_usd = to_usd(float(data.iloc[0]['Closing Price']))

	#Parse latest date

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
	timehigh = to_usd(timehigh)

	timelow = float(min(low_price))
	timelow = to_usd(timelow)

	# breakpoint()
	write_to_csv(data)

	# Pull market data based on stock market capitalization: 

	index_url = compile_url(index_ticker,api_key)
	index_response = requests.get(index_url)
	index_response_val = index_response.text
	if validate_response(index_response_val) == "Error":
		large_cap_index = "SPY"
		mid_cap_index = "RMCCX"
		small_cap_index = "^RUT"
		print("We ran into an error with your benchmark and unfortunately had to utilize the default benchmarks. Please redefine your stock.")
		define_stock()
		index_url = compile_url(index_ticker,api_key)
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
