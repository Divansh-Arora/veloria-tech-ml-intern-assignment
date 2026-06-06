from bs4 import BeautifulSoup
import pandas as pd

HTML_FILE = "india_vs_aus.html"

with open(HTML_FILE, "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

matches = []

table = soup.find("table", class_="TableLined")

rows = table.find_all("tr")

for row in rows[1:]:  # skip header

    cols = row.find_all("td")

    if len(cols) != 5:
        continue

    match_no = cols[0].get_text(strip=True)

    if not match_no.isdigit():
        continue

    date = cols[1].get_text(strip=True)
    series = cols[2].get_text(" ", strip=True)
    venue = cols[3].get_text(" ", strip=True)
    result = cols[4].get_text(" ", strip=True)

    matches.append({
        "date": date,
        "series": series,
        "venue": venue,
        "result": result
    })

df = pd.DataFrame(matches)

print(df.head())
print("\nTotal matches:", len(df))

df.to_csv("match_data.csv", index=False)

print("\nCSV saved successfully.")