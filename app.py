import yfinance as yf
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

# แสดงข้อมูลราคาล่าสุด
print(realtime_data.tail(5))