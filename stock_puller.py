import yfinance as yf

def get_stock_price():
    print("=== Welcome to the Stock Puller App ===")
    
    # 1. Ask the user to input a stock ticker symbol
    ticker_symbol = input("Enter a stock ticker (e.g., AAPL, TSLA, MSFT): ").upper()
    
    try:
        # 2. Connect to Yahoo Finance and pull the stock data
        stock = yf.Ticker(ticker_symbol)
        
        # 3. Request the current market price
        current_price = stock.fast_info['last_price']
        currency = stock.fast_info['currency']
        
        # 4. Display the results to the user
        print(f"\nThe current price of {ticker_symbol} is: {current_price:.2f} {currency}")
        
    except Exception as e:
        print("\n[Error] Could not find that ticker. Please check the spelling and try again.")

# Run the app
if __name__ == "__main__":
    get_stock_price()
