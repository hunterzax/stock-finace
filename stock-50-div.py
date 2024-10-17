import yfinance as yf
import pandas as pd

# รายชื่อหุ้นที่มีชื่อเสียงว่าจ่ายปันผลรายเดือน
# tickers = [
#     'O', 'MAIN', 'STAG', 'AGNC', 'PSEC', 
#     'SLG', 'EPR', 'LTC', 'ARR', 'GOOD', 
#     'HRZN', 'GAIN', 'LAND', 'GLAD', 'SPHD', 'DX'
# ]
tickers = [
    "O",    # Realty Income Corporation
    "STAG", # STAG Industrial, Inc.
    "LTC",  # LTC Properties, Inc.
    "SJR",  # Shaw Communications Inc.
    "EPR",  # EPR Properties
    "PBA",  # Pembina Pipeline Corporation
    "SKT",  # Tanger Factory Outlet Centers, Inc.
    "GNL",  # Global Net Lease, Inc.
    "IIPR", # Innovative Industrial Properties, Inc.
    "AGNC", # AGNC Investment Corp.
    "AFIN", # American Finance Trust, Inc.
    "CLDT", # Chatham Lodging Trust
    "CUZ",  # Cousins Properties Incorporated
    "DMB",  # Dreyfus Municipal Bond Infrastructure Fund
    "PFD",  # Flaherty & Crumrine Preferred Income Fund
    "GAIN", # Gladstone Investment Corporation
    "GOOD", # Gladstone Commercial Corporation
    "MAIN", # Main Street Capital Corporation
    "MFA",  # MFA Financial, Inc.
    "NYMT", # New York Mortgage Trust, Inc.
    "SACH", # Sachem Capital Corp
    "SIC",  # Sierra Income Corporation
    "TCI",  # Transcontinental Realty Investors, Inc.
    "DHC",  # Diversified Healthcare Trust
    "DCT",  # DCT Industrial Trust Inc.
    "BPY",  # Brookfield Property Partners L.P.
    "BXMT", # Blackstone Mortgage Trust, Inc.
    "CMCT", # CIM Commercial Trust Corporation
    "STWD", # Starwood Property Trust, Inc.
    "TGH",  # Tornado Global Hydrovacs Ltd.
    "OXSQ", # Oxford Square Capital Corp
    "ECC",  # Eagle Point Credit Company Inc.
    "FDUS", # Fidus Investment Corporation
    "PSEC", # Prospect Capital Corporation
    "HRZN", # Horizon Technology Finance Corporation
    "IVR",  # Invesco Mortgage Capital Inc.
    "XHR",  # Xenia Hotels & Resorts, Inc.
    "TLO",  # Talon Metals Corp.
    "VCF",  # Verde Clean Fuels, Inc.
    "TWO",  # Two Harbors Investment Corp.
    "AVH",  # Avianca Holdings S.A.
    "MDLY", # Medley Management Inc.
    "PYPL", # PayPal Holdings, Inc.
    "BKCC", # BlackRock Capital Investment Corporation
    "ECC",  # Eagle Point Credit Company Inc.
    "VNR",  # Vanguard Natural Resources, LLC
    "BXSL", # Blackstone Secured Lending Fund
    "LADR", # Ladder Capital Corp
    "HSRE", # Harrison Street Real Estate Investment Trust
    "ZNGA"  # Zynga Inc.
]

# ดึงข้อมูลหุ้นปันผลรายเดือน
monthly_dividend_stocks = []
for ticker in tickers:
    stock = yf.Ticker(ticker)
    # print(stock.history(period="1d"))
    try:
        # ดึงข้อมูลประวัติการจ่ายปันผล
        dividends = stock.dividends
        
        # ตรวจสอบว่าหุ้นนั้นจ่ายปันผลรายเดือนหรือไม่ (>= 12 ครั้งใน 1 ปี)
        if len(dividends) >= 12:
            info = stock.info
            # print(info)
            dividend_yield = info.get('dividendYield', None)
            current_price = info.get('currentPrice', 'N/A')
            
            # คำนวณจำนวนปีที่มีการจ่ายปันผลและจำนวนปีที่เพิ่มขึ้น
            if not dividends.empty:
                first_date = dividends.index.min().year
                last_date = dividends.index.max().year
                years_of_dividends = last_date - first_date + 1
                
                # คำนวณจำนวนปีที่มีการเพิ่มปันผล (ถ้ามีข้อมูลการเพิ่ม)
                annual_dividends = dividends.resample('YE').sum()
                years_increase = 0
                for i in range(1, len(annual_dividends)):
                    if annual_dividends.iloc[i] > annual_dividends.iloc[i - 1]:
                        years_increase += 1
            
            # ถ้ามี Dividend Yield ให้เพิ่มเข้าไปในรายการ
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
    # Calculate monthly dividend yield
    monthly_yield = row['Dividend Yield (%)'] / 100 / 12  # Convert to monthly yield
    if monthly_yield > 0:  # Ensure yield is not zero
        required_investment = desired_monthly_dividend / monthly_yield
        df.at[index, 'Required Investment ($)'] = required_investment
    else:
        df.at[index, 'Required Investment ($)'] = 'N/A'

# แสดงผล 50 อันดับแรกพร้อมจำนวนเงินที่ต้องลงทุน
print("Assuming you want : ",desired_monthly_dividend)
print(df[['Ticker', 'Name', 'Price', 'Dividend Yield (%)', 'Years of Dividend Increase','Required Investment ($)']].head(50))
