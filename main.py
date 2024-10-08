import requests
from creds import STOCK_API_KEY, NEWS_API_KEY

STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Get yesterday's closing stock price.

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price.
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Find the positive difference between the closing prices.
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

# Find the percentage difference between the closing prices.
diff_percentage = (difference / float(day_before_yesterday_closing_price)) * 100
print(diff_percentage)

# Get articles (news) with COMPANY_NAME if percentage difference is higher than e.g. 2%.
if diff_percentage > 1.5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Get first three articles using slicing operator.
    three_articles = articles[:3]
