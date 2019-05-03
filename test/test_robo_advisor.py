import datetime as dt
from dotenv import load_dotenv
import json
import os
import pandas as pd
import requests
import statistics as stat

from app.robo_advisor import *

def test_to_usd():
	result = to_usd(5200.2)
	assert result == "$5200.20"

def test_convert_month():
	a = convert_month(1)
	assert a == "January"
	b = convert_month(4)
	assert b == "April"
	c = convert_month(9)
	assert c == "September"
	d = convert_month(12)
	assert d == "December"

def test_compile_url():
	result = compile_url("AAPL","TEST_KEY_STRING")
	assert result == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=TEST_KEY_STRING"