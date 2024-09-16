import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up API key from environment variable
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query?"

# Function to get stock information (volume, highs, lows, etc.)
def get_stock_info(ticker):
    function = "TIME_SERIES_DAILY"
    url = f"{BASE_URL}function={function}&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Check if the "Time Series (Daily)" key exists in the response
        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            
            # Extract the latest date and stock data
            latest_date = list(time_series.keys())[0]
            latest_data = time_series[latest_date]
            
            # Extract and return relevant information
            return {
                "Date": latest_date,
                "Open": latest_data["1. open"],
                "High": latest_data["2. high"],
                "Low": latest_data["3. low"],
                "Close": latest_data["4. close"],
                "Volume": latest_data["5. volume"]
            }
        else:
            return {"Error": "Time series data not found in the response"}
    else:
        return {"Error": "Failed to retrieve data from Alpha Vantage"}

# Function to get cash flow data
def get_cash_flow(ticker):
    function = "CASH_FLOW"
    url = f"{BASE_URL}function={function}&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "annualReports" in data:
        return data["annualReports"]
    else:
        return {"Error": "Failed to retrieve cash flow information"}

# Function to get balance sheet data
def get_balance_sheet(ticker):
    function = "BALANCE_SHEET"
    url = f"{BASE_URL}function={function}&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "annualReports" in data:
        return data["annualReports"]
    else:
        return {"Error": "Failed to retrieve balance sheet information"}

# Function to get recent news
def get_recent_news(ticker):
    function = "NEWS_SENTIMENT"
    url = f"{BASE_URL}function={function}&tickers={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "feed" in data:
        return data["feed"][:5]  # Returning top 5 news stories
    else:
        return {"Error": "Failed to retrieve news information"}

# Function to save data in a formatted way
def save_data_to_file(data, filename="apple_stock_report.txt"):
    with open(filename, 'w') as f:
        f.write(data)

# Main function to fetch all data for Apple stock and format it
def get_apple_stock_data():
    ticker = "AAPL"
    
    # Get stock ticker information
    stock_info = get_stock_info(ticker)
    stock_info_str = f"Stock Information for {ticker}:\n"
    stock_info_str += f"Date: {stock_info.get('Date')}\n"
    stock_info_str += f"Open: {stock_info.get('Open')}\n"
    stock_info_str += f"High: {stock_info.get('High')}\n"
    stock_info_str += f"Low: {stock_info.get('Low')}\n"
    stock_info_str += f"Close: {stock_info.get('Close')}\n"
    stock_info_str += f"Volume: {stock_info.get('Volume')}\n\n"
    
    # Get cash flow information
    cash_flow_info = get_cash_flow(ticker)
    cash_flow_str = "Cash Flow Information:\n"
    if isinstance(cash_flow_info, list):
        for report in cash_flow_info[:2]:  # Get the last 2 years of reports
            cash_flow_str += f"Fiscal Year: {report.get('fiscalDateEnding')}\n"
            cash_flow_str += f"Operating Cash Flow: {report.get('operatingCashflow')}\n"
            cash_flow_str += f"Capital Expenditures: {report.get('capitalExpenditures')}\n"
            cash_flow_str += f"Cash Flow from Financing: {report.get('cashflowFromFinancing')}\n\n"
    else:
        cash_flow_str += cash_flow_info["Error"] + "\n\n"
    
    # Get balance sheet information
    balance_sheet_info = get_balance_sheet(ticker)
    balance_sheet_str = "Balance Sheet Information:\n"
    if isinstance(balance_sheet_info, list):
        for report in balance_sheet_info[:2]:  # Get the last 2 years of reports
            balance_sheet_str += f"Fiscal Year: {report.get('fiscalDateEnding')}\n"
            balance_sheet_str += f"Total Assets: {report.get('totalAssets')}\n"
            balance_sheet_str += f"Total Liabilities: {report.get('totalLiabilities')}\n"
            balance_sheet_str += f"Total Shareholder Equity: {report.get('totalShareholderEquity')}\n\n"
    else:
        balance_sheet_str += balance_sheet_info["Error"] + "\n\n"
    
    # Get recent news
    news_info = get_recent_news(ticker)
    news_str = "Recent News:\n"
    if isinstance(news_info, list):
        for i, news in enumerate(news_info, 1):
            news_str += f"News {i}:\n"
            news_str += f"Title: {news.get('title')}\n"
            news_str += f"Summary: {news.get('summary')}\n"
            news_str += f"URL: {news.get('url')}\n\n"
    else:
        news_str += news_info["Error"] + "\n\n"
    
    # Combine all sections into a single report
    full_report = stock_info_str + cash_flow_str + balance_sheet_str + news_str
    
    # Save the report to a file
    save_data_to_file(full_report)
    print(f"Report saved as 'apple_stock_report.txt'.")

if __name__ == "__main__":
    get_apple_stock_data()
