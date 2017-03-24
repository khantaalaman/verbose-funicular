import json
import csv

print "Starting SIMULATION..."

with open('quotes.json') as json_data:
    data = json.load(json_data)
    dates = []
    for agroup in data:
        for thedate in agroup.keys():
            dates.append(thedate)
    #get ordered dates
    dates = sorted(dates, reverse=True)

    #for sanitizing data. Yeah taking the longer route only for testing purposes.
    di = []
    for adate in dates:
        for againgroup in data:
            for againdate in againgroup.values():
                if adate == againdate[0]:
                    ki = {}
                    ki["date"] = againdate[0]
                    ki["second"] = againdate[1]
                    ki["third"] = againdate[2]
                    ki["fourth"] = againdate[3]
                    di.append(ki)


print "Loading PRICES..."

with open('prices.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    ni = []

    for row in readCSV:
        for anelement in di:
            if anelement["date"] == row[0]:
                ki = {}
                ki["date"] = anelement["date"]
                ki["price"] = row[1]
                ki["macd"] = anelement["second"]
                ki["ema9"] = anelement["third"]
                ni.append(ki)


leli = ni

num_day = 30

results = []

popo = 0

for popo in range(1720):
    ni = leli[(1720-popo):(1750-popo)]

    this_date = leli[(1719-popo)]["date"]
    price_this_date = leli[(1719-popo)]["price"]

    print "Analysing SMA-20 Slope..."

    # Analysing SMA-20's Slope on the present day. Here it will be 1/02/2017 as per the database available.

    ####Calculating SMA20 for Today####

    sum = 0

    for ani in range(20):
        sum += float(ni[ani]["price"])

    sma_today = sum / 20

    ####Calculating SMA20 for a day before####

    sum = 0

    for ani in range(21):
        if ani == 0:
            continue
        sum += float(ni[ani]["price"])

    sma_adaybefore = sum / 20

    diff = sma_adaybefore - sma_today

    if diff > 0:
        results.append({"backtest_date": this_date, "result": "BUY", "price": price_this_date, "test_name": "SMA-20"})
    elif diff < 0:
        results.append({"backtest_date": this_date, "result": "SELL", "price": price_this_date, "test_name": "SMA-20"})
    else:
        results.append({"backtest_date": this_date, "result": " ", "price": price_this_date, "test_name": "SMA-20"})

print results

ofile  = open('SMA-20_backtest.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
for aresult in results:
    row_list = []
    row_list.append(aresult["backtest_date"])
    row_list.append(aresult["result"])
    row_list.append(aresult["price"])
    row_list.append(aresult["test_name"])
    writer.writerow(row_list)

ofile.close()