import csv
import matplotlib.pyplot as plt
from datetime import datetime
#lists to store our data
dates = []
prices=[]

# Read the csv file data
with open ('Oil prices for computational physics.csv', 'r') as file:
	reader = csv.reader(file)

	for row in reader:
		if not row or row[0].startswith('#'):
			continue
		if row[0] == 'Date':
			continue
		date_obj = datetime.strptime(row[0], '%m/%d/%Y')
		price_val = float(row[1])


		dates.append(date_obj)
		prices.append(price_val)

#sort data
sorted_data = sorted(zip(dates, prices))
dates = [x[0] for x in sorted_data]
prices = [x[1] for x in sorted_data]

moving_averages = []
window_size = 12

for i in range (len(prices)):
	if i < window_size - 1:
		moving_averages.append(None)
	else:
		window_slice = prices [i - window_size + 1 :i + 1]
		window_average = sum(window_slice) / window_size
		moving_averages.append(window_average)
events = [
	("1973 Oil Crisis", datetime(1973, 10, 1)),
	("1978 Oil Shock", datetime(1979,1,1)),
	("1986 Oil Price Collapse", datetime(1986, 1, 1)),
	("1999 OPEC Production Cuts", datetime(1999, 1, 1)),
	("2008 Financial Crisis", datetime(2008, 9, 1)),
	("2016 Oil Prices Fall", datetime(2016, 1, 1)),
	("2020 Covid Crisis", datetime(2020, 7, 1))
]
plt.figure(figsize=(10,6))
plt.plot(dates, moving_averages, label = '12 Month Moving Average', color = 'black')
#add event markers
for label, event_date in events:
	if dates[0] <= dates[-1]:
		plt.axvline(event_date, linestyle='--', alpha=0.6)
		plt.text(event_date, max(prices)*0.8, label, rotation=90, fontsize = 8)
plt.ylim(min(prices), max(prices) * 1.25)
# --- NEW: Calculate Percentage Change Between Events ---

# 1. Identify prices at each event date
event_summary = []
for label, event_date in events:
    # Ensure the event date is within our data range
    if dates[0] <= event_date <= dates[-1]:
        # Find the index of the date in our list closest to the event date
        closest_date = min(dates, key=lambda d: abs(d - event_date))
        idx = dates.index(closest_date)
        price_at_event = prices[idx]
        event_summary.append({'label': label, 'date': event_date, 'price': price_at_event})

# 2. Calculate and print changes between consecutive events
print("\n" + "="*50)
print(f"{'EVENT TRANSITION':<40} | {'% CHANGE':<10}")
print("="*50)

for i in range(1, len(event_summary)):
    prev = event_summary[i-1]
    curr = event_summary[i]

    # Percentage Change Formula: ((New - Old) / Old) * 100
    pct_change = ((curr['price'] - prev['price']) / prev['price']) * 100

    transition_label = f"{prev['label']} -> {curr['label']}"
    print(f"{transition_label[:40]:<40} | {pct_change:+.2f}%")

print("="*50)
plt.title('Historical Oil Prices (12 Month Moving Average analysis')
plt.xlabel('year')
plt.ylabel('price')
plt.legend()
plt.grid(True)
plt.savefig('oil_prices_plot.pdf')
plt.show()
print("Analysis complete")
