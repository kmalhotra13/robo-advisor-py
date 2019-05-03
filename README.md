# "Robo Advisor" Project [![Build Status](https://travis-ci.com/kmalhotra13/robo-advisor-py.svg?branch=master)](https://travis-ci.com/kmalhotra13/robo-advisor-py)

Issues requests to the [AlphaVantage Stock Market API](https://www.alphavantage.co/) in order to provide automated stock or cryptocurrency trading recommendations.

## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip

### Required Python Packages & Modules:

  + datetime
  + dotenv
  + json
  + os
  + pandas
  + requests
  + statistics

## Installation

In order to set up this applet, please download install the source code:

```sh
git clone git@github.com:kmalhotra/robo-advisor-py
cd robo-advisor-py/
```

Install the package dependencies:

```sh
pip install -r requirements.txt
```

## Setup

Before using or developing this application, take a moment to [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key) (e.g. "abc123").

After obtaining an API Key, copy the ".env.example" file to a new file called ".env", and update the contents of the ".env" file to specify your real API Key. (Don't worry, the ".env" has already been [ignored](/.gitignore) from version control for you!)

Navigate in the command prompt to the appropriate repository directory that contains the python script.

## Usage

Run the recommendation script:

```py
python app/robo_advisor.py
```
The command prompt will ask you to enter in a ticker symbol or a menu option:
  + **'settings':** This will allow you to change the benchmark index funds against which the recommendations are made. 
    + The default configuration is to benchmark Large Cap stocks against the S&P 500, Mid Cap stocks against the Russell Mid Cap Fund, and Small Cap stocks against the Russell 2000 Index. 
    + After you change your benchmarks, the program will redirect you to the main selection prompt.
    + If the benchmark you entered cannot be found, the program will run automatically against the default benchmarks.
  + **'exit':** Typing this will exit the program. 
  + **Any Ticker:** Entering any ticker in will run the program to create a recommendation for that ticker. 
  	+ _Keep in mind that if the ticker you enter is blank or too long, it will ask you for a new one, and if it is of appropriate length but cannot be found, the program will exit._

After that, you will be asked to identify the class of the stock based on the market capitalization, so the program can run its statistics against a benchmark index. 

Then, the program will generate a recommendation based on the Sharpe ratios of the stock and the index; if the stock has a higher Sharpe ratio, it will recommend a 'Buy.'

## Testing

From within the virtual environment, install the `pytest` package (first time only):

```sh
pip install pytest
```

Run tests:

```sh
pytest
```


-----

_**Disclaimer**: the creators of this script bear no liability for gains/losses from on investments made based on provided recommendations._





## [License](/LICENSE.md)
