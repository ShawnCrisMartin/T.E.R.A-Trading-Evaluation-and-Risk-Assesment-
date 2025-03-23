import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from termcolor import colored  # For color in the terminal

# Alpha Vantage API key (replace 'your_api_key' with your actual key)
api_key = 'your_api_key'

# Function to fetch stock data
def fetch_data(symbol):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, _ = ts.get_daily(symbol=symbol, outputsize='full')
    return data

# Function to calculate risk metrics
def calculate_risk_metrics(stock_data):
    # Calculate daily returns
    stock_data['return'] = stock_data['4. close'].pct_change()
    
    # Calculate average daily return (mean)
    mean_return = stock_data['return'].mean()
    
    # Calculate volatility (standard deviation of daily returns)
    volatility = stock_data['return'].std()
    
    # Calculate Value at Risk (VaR) at 95% confidence level
    VaR_95 = stock_data['return'].quantile(0.05)
    
    return mean_return, volatility, VaR_95

# Function to visualize stock data and risk assessment
def plot_risk_assessment(stock_data):
    # Set a more aesthetic style
    plt.style.use('ggplot')
    
    # Create a figure with a yellow background
    plt.figure(figsize=(10, 6), facecolor='yellow')
    
    # Plot the stock price with a refined line style and color
    plt.plot(stock_data.index, stock_data['4. close'], label='Stock Price (Closing)', color='#1f77b4', linewidth=2, linestyle='--')

    # Title and labels with custom styling
    plt.title('Stock Price Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)

    # Customize the ticks on the x-axis for better readability
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    
    # Add a grid with customized properties
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Add legend
    plt.legend(loc='upper left', fontsize=12)

    # Show plot
    plt.tight_layout()  # To ensure everything fits within the figure
    plt.show()



# Function to display the risk assessment with color in the terminal
def display_risk_assessment(symbol, mean_return, volatility, VaR_95, stock_data):
    print(colored(f"Risk Assessment for {symbol}:", 'green'))
    print(colored(f"Mean Daily Return: {mean_return:.5f}", 'blue'))
    print(colored(f"Volatility (Standard Deviation of Returns): {volatility:.5f}", 'yellow'))
    print(colored(f"Value at Risk (95% confidence): {VaR_95:.5f}", 'red'))
    
    # Display suggestion based on VaR
    if VaR_95 < -0.02:
        print(colored("Suggestion: SELL", 'red'))
    elif VaR_95 > 0.02:
        print(colored("Suggestion: BUY", 'green'))
    else:
        print(colored("Suggestion: HOLD", 'yellow'))
    
    # Plot the stock data with improved aesthetics
    plot_risk_assessment(stock_data)

# Main function
def main():
    symbol = 'AAPL'  # Example: Apple stock
    stock_data = fetch_data(symbol)
    
    # Perform risk analysis
    mean_return, volatility, VaR_95 = calculate_risk_metrics(stock_data)
    
    # Call function to display risk assessment and suggestion
    display_risk_assessment(symbol, mean_return, volatility, VaR_95, stock_data)

if __name__ == "__main__":
    main()
