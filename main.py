import requests
from creds import STOCK_API_KEY, NEWS_API_KEY, TWILIO_SID, TWILIO_AUTH_TOKEN, MY_PHONE_NUMBER, MY_TWILIO_TEST_NUMBER
from twilio.rest import Client

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

# Find the difference between the closing prices.
difference = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)
up_down = None
if difference > 0:
    up_down = "🚀"
else:
    up_down = "🔻"

# Find the percentage difference between the closing prices.
diff_percentage = round(difference / float(day_before_yesterday_closing_price) * 100, 2)
print(diff_percentage)

# Get articles (news) with COMPANY_NAME if percentage difference is higher than e.g. 2%.
if abs(diff_percentage) > 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Get first three articles using slicing operator.
    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percentage}% \nHeadline: {article['title']} "
                          f"\nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)

    # Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=MY_TWILIO_TEST_NUMBER,
            to=MY_PHONE_NUMBER
        )