import yfinance as yf
import pandas as pd

# url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
# tables = pd.read_html(url)
# sp500_symbols = tables[0]['Symbol'].tolist()


# รายชื่อหุ้นที่มีชื่อเสียงว่าจ่ายปันผลรายเดือน
tickers = [
    'O', 'MAIN', 'STAG', 'AGNC', 'PSEC', 
    'SLG', 'EPR', 'LTC', 'ARR', 'GOOD', 
    'HRZN', 'GAIN', 'LAND', 'GLAD', 'SPHD','DX'
]

# ดึงข้อมูลหุ้นปันผล
monthly_dividend_stocks = []
for ticker in tickers:
    stock = yf.Ticker(ticker)
    try:
        # ดึงข้อมูลหุ้น
        info = stock.info
        dividend_yield = info.get('dividendYield', None)
        
        # ถ้ามี Dividend Yield ให้เพิ่มเข้าไปในรายการ
        if dividend_yield:
            monthly_dividend_stocks.append({
                'Ticker': ticker,
                'Name': info.get('longName', 'N/A'),
                'Price':info.get('regularMarketPrice','N/A'),
                'Dividend Yield (%)': dividend_yield * 100
            })
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

# สร้าง DataFrame และเรียงลำดับตาม Dividend Yield
df = pd.DataFrame(monthly_dividend_stocks)
df = df.sort_values(by='Dividend Yield (%)', ascending=False)

# แสดง 10 อันดับแรก
print(df.head(20))
