import yfinance as yf
import pandas as pd

data = {}

stock = yf.Ticker("DX")

# ดึงข้อมูลเกี่ยวกับหุ้นเพิ่มเติม
info = stock.info

# แสดงข้อมูลพื้นฐาน
print(f"ชื่อบริษัท: {info['longName']}")
# print(f"ราคาปัจจุบัน: {info['regularMarketPrice']}")
print(f"ปริมาณการซื้อขาย: {info['volume']}")
print(f"อัตราส่วน PE: {info['trailingPE']}")

# data = yf.Ticker("msft", start_date="12/04/2009", end_date="12/04/2019", index_as_date = True, interval="1wk")
# msft.actions
# ดึงข้อมูลตาม Period
mdata = stock.history(start="2024-10-15", end="2024-10-18", interval="1d") 
# vdata = msft.
# ดึวข้อมูลล่าสุด
#realtime_data = msft.history(period="max")

# ดึงข้อมูลแบบเรียลไทม์
realtime_data = stock.history(period="1d", interval="1m")

# ดึงข้อมูลจาก Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)
sp500_symbols = tables[0]['Symbol'].tolist()


# แสดงสัญลักษณ์หุ้นทั้งหมด
print(sp500_symbols)
print("จำนวนหุ้นใน S&P 500:", len(sp500_symbols))

tickers = ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'GOOGL', 'F', 'T', 'GE']
# ดึงราคาปิดล่าสุดของหุ้นทั้งหมด
for ticker in sp500_symbols:
    try:
        stock = yf.Ticker(ticker)
        data[ticker] = stock.history(period='1d')['Close'].iloc[-1]

# แปลงข้อมูลเป็น DataFrame เพื่อดูหุ้นที่ราคาถูกที่สุด
df = pd.DataFrame(list(data.items()), columns=['Ticker', 'Price'])
df = df.sort_values(by='Price')
print(df)