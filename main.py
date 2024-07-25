import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "[MY_STOCK_API_KEY]"
NEWS_API_KEY = "[MY_NEWS_API_KEY]"
THRESHOLD_VALUE = 10  # Desired threshold value of stock price difference in the last two days

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = "[MY_TWILIO_SID]"
TWILIO_AUTH_TOKEN = "[MY_TWILIO_AUTH_TOKEN]"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday = data_list[0]
yesterday_closing_price = yesterday["4. close"]

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = "⬆️" if difference > 0 else "⬇️"
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > THRESHOLD_VALUE:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_articles = [
        f"""{STOCK_NAME}: {up_down} {diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"""
        for article in three_articles
    ]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="[YOUR_TWILIO_VIRTUAL_NUMBER]",
            to="[YOUR_NUMBER]"
        )
