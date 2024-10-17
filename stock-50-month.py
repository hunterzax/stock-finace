import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored, cprint
from colorama import *

# รายชื่อหุ้นที่มีชื่อเสียงว่าจ่ายปันผลรายเดือน
tickers = [
    "O",    # Realty Income Corporation
    "STAG", # STAG Industrial, Inc.
    "LTC",  # LTC Properties, Inc.
    "EPR",  # EPR Properties
    "AGNC", # AGNC Investment Corp.
    "MAIN", # Main Street Capital Corporation
    "NYMT", # New York Mortgage Trust, Inc.
    "GAIN", # Gladstone Investment Corporation
    "SIC",  # Sierra Income Corporation
    "CLDT",  # Chatham Lodging Trust
    "DX"    # Dynex Capital, Inc.
]

# ดึงข้อมูลหุ้นปันผลรายเดือน
monthly_dividend_stocks = []
for ticker in tickers:
    stock = yf.Ticker(ticker)
    try:
        dividends = stock.dividends
        
        if len(dividends) >= 12:
            info = stock.info
            dividend_yield = info.get('dividendYield', None)
            current_price = info.get('currentPrice', 'N/A')
            
            if not dividends.empty:
                first_date = dividends.index.min().year
                last_date = dividends.index.max().year
                years_of_dividends = last_date - first_date + 1
                
                annual_dividends = dividends.resample('YE').sum()
                years_increase = 0
                for i in range(1, len(annual_dividends)):
                    if annual_dividends.iloc[i] > annual_dividends.iloc[i - 1]:
                        years_increase += 1
            
            if dividend_yield:
                monthly_dividend_stocks.append({
                    'Ticker': ticker,
                    'Name': info.get('longName', 'N/A'),
                    'Price': current_price,
                    'Dividend Yield (%)': dividend_yield * 100,
                    'Years of Dividends': years_of_dividends,
                    'Years of Dividend Increase': years_increase
                })
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

# สร้าง DataFrame และเรียงลำดับตาม Dividend Yield
df = pd.DataFrame(monthly_dividend_stocks)
df = df.sort_values(by='Dividend Yield (%)', ascending=False)

# Assuming you want $10 in monthly dividends
desired_monthly_dividend = 10 

# Calculate required investment for each stock
for index, row in df.iterrows():
    monthly_yield = row['Dividend Yield (%)'] / 100 / 12  # Convert to monthly yield
    if monthly_yield > 0:  
        required_investment = desired_monthly_dividend / monthly_yield
        df.at[index, 'Required Investment ($)'] = required_investment
    else:
        df.at[index, 'Required Investment ($)'] = 'N/A'

# แสดงผล 50 อันดับแรกพร้อมจำนวนเงินที่ต้องลงทุน
print(Fore.RED+"------------------------------------------------")
print(Fore.LIGHTBLUE_EX+"Assuming you want : ",desired_monthly_dividend)
print(Fore.RED+"------------------------------------------------"+Fore.WHITE)

print(df[['Ticker', 'Name', 'Price', 'Dividend Yield (%)', 'Years of Dividend Increase', 'Required Investment ($)']].head(50))

# Visualization
top_n = 10  # Adjust this to show more or fewer stocks
df_top = df.head(top_n)

plt.figure(figsize=(12, 6))
plt.bar(df_top['Ticker'], df_top['Required Investment ($)'], color='blue', alpha=0.7, label='Required Investment ($)')
plt.ylabel('Required Investment ($)')
plt.title('Required Investment to Achieve $10 Monthly Dividend by Stock')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Show plot
plt.show()
