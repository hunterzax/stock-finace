import yfinance as yf
import pandas as pd

# ดึงข้อมูลจาก S&P 500 ผ่าน Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)
sp500_symbols = tables[0]['Symbol'].tolist()

# แก้ชื่อสัญลักษณ์ให้ถูกต้องสำหรับ Yahoo Finance
sp500_symbols = [symbol.replace('.', '-') for symbol in sp500_symbols]

# ดึงข้อมูลหุ้นปันผล
dividend_stocks = []
for ticker in sp500_symbols:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        dividend_yield = info.get('dividendYield', None)
        
        # ถ้าหุ้นมีอัตราปันผล (ไม่ใช่ None) และมากกว่า 0 ให้เพิ่มในรายการ
        if dividend_yield and dividend_yield > 0:
            dividend_stocks.append({
                'Ticker': ticker,
                'Name': info.get('longName', 'N/A'),
                'Dividend Yield': dividend_yield * 100
            })
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

# สร้าง DataFrame และแสดงผลหุ้นปันผล
dividend_df = pd.DataFrame(dividend_stocks)
dividend_df = dividend_df.sort_values(by='Dividend Yield', ascending=False)
print(dividend_df)


# ดึงข้อมูลปันผลจากหุ้นที่กำหนดไว้
monthly_dividend_stocks = []
for ticker in sp500_symbols:
    stock = yf.Ticker(ticker)
    try:
        # ดึงข้อมูลประวัติการจ่ายปันผล
        dividends = stock.dividends
        
        # ตรวจสอบความถี่การจ่ายปันผล
        if len(dividends) >= 12:  # มากกว่า 12 ครั้งต่อปี อาจเป็นการจ่ายรายเดือน
            monthly_dividend_stocks.append({
                'Ticker': ticker,
                'Name': stock.info.get('longName', 'N/A'),
                'Dividend Yield': stock.info.get('dividendYield', None) * 100
            })
    except Exception as e:
        print(f"Error with {ticker}: {e}")

# สร้าง DataFrame และแสดงผล
df = pd.DataFrame(monthly_dividend_stocks)
print(df)
