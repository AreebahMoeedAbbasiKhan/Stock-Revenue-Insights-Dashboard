
# ============================
# IMPORT LIBRARIES
# ============================
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go

# ============================
# TESLA STOCK DATA
# ============================
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")

tesla_data.reset_index(inplace=True)

print("Tesla Stock Data:")
print(tesla_data.head())


# ============================
# TESLA REVENUE DATA
# ============================
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/data/tesla_revenue.html"

html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html.parser")

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

tables = soup.find_all("table")

for table in tables:
    if "Tesla Quarterly Revenue" in table.text:
        rows = table.find_all("tr")
        
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) != 0:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip()
                tesla_revenue.loc[len(tesla_revenue)] = [date, revenue]

# Clean revenue data
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(",", "")
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace("$", "")
tesla_revenue.dropna(inplace=True)

print("\nTesla Revenue Data:")
print(tesla_revenue.tail())


# ============================
# GAMESTOP STOCK DATA
# ============================
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")

gme_data.reset_index(inplace=True)

print("\nGameStop Stock Data:")
print(gme_data.head())


# ============================
# GAMESTOP REVENUE DATA
# ============================
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/data/gme_revenue.html"

html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html.parser")

gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

tables = soup.find_all("table")

for table in tables:
    if "GameStop Quarterly Revenue" in table.text:
        rows = table.find_all("tr")
        
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) != 0:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip()
                gme_revenue.loc[len(gme_revenue)] = [date, revenue]

# Clean revenue data
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(",", "")
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace("$", "")
gme_revenue.dropna(inplace=True)

print("\nGameStop Revenue Data:")
print(gme_revenue.tail())


# ============================
# DASHBOARD FUNCTION
# ============================
def make_graph(stock_data, revenue_data, title):
    
    # Convert revenue to numeric
    revenue_data["Revenue"] = pd.to_numeric(revenue_data["Revenue"])
    revenue_data["Date"] = pd.to_datetime(revenue_data["Date"])
    
    fig = go.Figure()

    # Stock price line
    fig.add_trace(go.Scatter(
        x=stock_data["Date"],
        y=stock_data["Close"],
        name="Stock Price",
        mode="lines"
    ))

    # Revenue line
    fig.add_trace(go.Scatter(
        x=revenue_data["Date"],
        y=revenue_data["Revenue"],
        name="Revenue",
        mode="lines"
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_white"
    )

    fig.show()


# ============================
# TESLA DASHBOARD
# ============================
make_graph(tesla_data, tesla_revenue, "Tesla Stock Price vs Revenue")


# ============================
# GAMESTOP DASHBOARD
# ============================
make_graph(gme_data, gme_revenue, "GameStop Stock Price vs Revenue")