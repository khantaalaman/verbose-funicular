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

with open('quotes-bollinger.json') as json_data_bollinger:
    data_bollinger = json.load(json_data_bollinger)

    # for changing format of data. Yeah taking the longer route only for testing purposes.
    di_bollinger = []
    for adate in dates:
        for againgroup in data_bollinger:
            for againdate in againgroup.values():
                if adate == againdate[0]:
                    ki = {}
                    ki["date"] = againdate[0]
                    ki["upper_band"] = againdate[2]
                    ki["middle_band"] = againdate[3]
                    ki["lower_band"] = againdate[4]
                    for aele in ni:
                        avar = 0
                        if aele["date"] == adate:
                            ki["price"] = aele["price"]
                    di_bollinger.append(ki)

leli = di_bollinger

for popo in range(1720):

    this_date = leli[(1719 - popo)]["date"]

    di_bollinger = leli[(1720 - popo):(1750 - popo)]

    boll_array = []

    for anele in range(num_day):
        boll_array.append(di_bollinger[anele])

    boll_array = [x for x in boll_array[::-1]]

    # print boll_array

    boll_list = []

    for k in range(len(boll_array)):
        try:
            if boll_array[k]["price"] < boll_array[k + 1]["price"] and boll_array[k + 1]["price"] > boll_array[k + 2][
                "price"]:
                boll_list.append({"MAX": boll_array[k + 1]})
            if boll_array[k]["price"] > boll_array[k + 1]["price"] and boll_array[k + 1]["price"] < boll_array[k + 2][
                "price"]:
                boll_list.append({"MIN": boll_array[k + 1]})
        except:
            continue

    # print boll_list

    for k in range(len(boll_list)):
        try:
            if boll_list[k].keys()[0] == "MAX" and boll_list[k + 1].keys()[0] == "MIN" and boll_list[k + 2].keys()[
                0] == "MAX":
                if float(boll_list[k].values()[0]["price"]) > float(boll_list[k + 2].values()[0]["price"]):
                    print "Finding sell condition after date: " + boll_list[k + 1].values()[0]["date"]
                    compare_value = float(boll_list[k + 1].values()[0]["price"])
                    for athing in boll_list[k + 1::]:
                        if float(athing.values()[0]["price"]) < compare_value:
                            print "Sell condition on date: " + athing.values()[0]["date"]
                            results.append({"backtest_date": this_date, "test_name": "MACD", "result": "SELL",
                                            "operate_on": athing.values()[0]["date"]})
                            break
            if boll_list[k].keys()[0] == "MIN" and boll_list[k + 1].keys()[0] == "MAX" and boll_list[k + 2].keys()[
                0] == "MIN":
                if float(boll_list[k].values()[0]["price"]) < float(boll_list[k + 2].values()[0]["price"]):
                    print "Finding buy condition after date: " + boll_list[k + 1].values()[0]["date"]
                    compare_value = float(boll_list[k + 1].values()[0]["price"])
                    for athing in boll_list[k + 1::]:
                        if float(athing.values()[0]["price"]) > compare_value:
                            print "Buy condition on date: " + athing.values()[0]["date"]
                            results.append({"backtest_date": this_date, "test_name": "MACD", "result": "BUY",
                                            "operate_on": athing.values()[0]["date"]})
                            break
        except:
            pass

print results