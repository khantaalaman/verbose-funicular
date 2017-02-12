import json
import csv
import matplotlib.pyplot as plt


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

num_day = input("Number of days to consider = ")

prices = []
macds = []
ema9 = []

for i in range(num_day):
    prices.append([float(ni[i]["price"]),ni[i]["date"]])
    macds.append([float(ni[i]["macd"]),ni[i]["date"]])
    ema9.append([float(ni[i]["ema9"]),ni[i]["date"]])

#checking and storing minimas

prices_minimas = []
macd_minimas = []

for k in range(len(prices)):
    try:
        if prices[k][0] < prices[k-1][0] and prices[k][0] < prices[k+1][0]:
            prices_minimas.append(prices[k])
        else:
            pass
    except:
        pass


for t in range(len(macds)):
    try:
        if macds[t][0] < macds[t-1][0] and macds[t][0] < macds[t+1][0]:
            macd_minimas.append(prices[t])
        else:
            pass
    except:
        pass


print prices_minimas
print macd_minimas

buy_con = []
sel_con = []


for amin in range(len(prices_minimas)):
    try:
        if prices_minimas[amin] < prices_minimas[amin + 1]:
            pass
        else:
            buy_con.append(0)
            print "Price analysis failed for Buy condition."
            break
    except:
        pass


for dmin in range(len(macd_minimas)):
    try:
        if macd_minimas[dmin] > macd_minimas[dmin + 1]:
            pass
        else:
            buy_con.append(0)
            print "MACD analysis failed for Buy condition"
            break
    except:
        pass


for hmin in range(len(prices_minimas)):
    try:
        if prices_minimas[hmin] > prices_minimas[hmin + 1]:
            pass
        else:
            sel_con.append(0)
            print "Price analysis failed for Sell condition."
            break
    except:
        pass


for nmin in range(len(macd_minimas)):
    try:
        if macd_minimas[nmin] < macd_minimas[nmin + 1]:
            pass
        else:
            sel_con.append(0)
            print "MACD analysis failed for Sell condition."
            break
    except:
        pass


if float(ni[0]["macd"]) == float(ni[0]["ema9"]):
    main_var = "CONTINUE"
if float(ni[0]["macd"]) < float(ni[0]["ema9"]):
    main_var = "less"
if float(ni[0]["macd"]) > float(ni[0]["ema9"]):
    main_var = "more"

cross_list = []


for aval in range(num_day):
    #if float(aval["macd"]) == float(aval["ema9"])... This condition has to be developed for future.
    if float(ni[aval]["macd"]) == float(ni[aval]["ema9"]):
        print "OOPS! The unexpected happened!"
        break
    if float(ni[aval]["macd"]) < float(ni[aval]["ema9"]):
        new_con = "less"
    elif float(ni[aval]["macd"]) > float(ni[aval]["ema9"]):
        new_con = "more"
    if main_var == "more" and new_con == "less":
        cross_list.append("cross_macd_now_less")
        main_var = "less"
        print "Cross Date: " + ni[aval]["date"]
    else:
        pass
    if main_var == "less" and new_con == "more":
        cross_list.append("cross_macd_now_high")
        main_var = "more"
        print "Cross Date: " + ni[aval]["date"]
    else:
        pass


if len(cross_list) == 0:
    print "No cross occurs"
elif len(cross_list) == 1:
    if cross_list[0] == "cross_macd_now_less":
        print "You must SELL as per line-cross analysis."
    if cross_list[0] == "cross_macd_now_high":
        print "You must BUY as per line-cross analysis."
elif len(cross_list) > 1:
    print "More than one cross. We will figure it out soon! :P"
else:
    pass


print cross_list

with open('quotes-1.json') as json_data_stck:
    data_stck = json.load(json_data_stck)

    #for changing format of data. Yeah taking the longer route only for testing purposes.
    di_stck = []
    for adate in dates:
        for againgroup in data_stck:
            for againdate in againgroup.values():
                if adate == againdate[0]:
                    ki = {}
                    ki["date"] = againdate[0]
                    ki["slow_k"] = againdate[1]
                    ki["slow_d"] = againdate[2]
                    di_stck.append(ki)

#the D-line analysis

if float(di_stck[0]["slow_d"]) < 20:
    main_val = "less_than_20"
if 20 < float(di_stck[0]["slow_d"]) < 80:
    main_val = "but_less_than_80"
if float(di_stck[0]["slow_d"]) > 80:
    main_val = "less_than_none"

cross_check_list = []


for aval in range(num_day):
    if float(di_stck[aval]["slow_d"]) < 20:
        check_val = "less_than_20"
    if 20 < float(di_stck[aval]["slow_d"]) < 80:
        check_val = "but_less_than_80"
    if float(di_stck[aval]["slow_d"]) > 80:
        check_val = "less_than_none"
    if main_val != check_val:
        cross_check_list.append([di_stck[aval]["date"], main_val, check_val])
        main_val = check_val

print cross_check_list

#End of D-line Analysis.

#Analysing SMA-20's Slope on the present day. Here it will be 1/02/2017 as per the database available.

####Calculating SMA20 for Today####

sum = 0

for ani in range(20):
    sum += float(ni[ani]["price"])

sma_today = sum/20

####Calculating SMA20 for a day before####

sum = 0

for ani in range(21):
    if ani == 0:
        continue
    sum += float(ni[ani]["price"])

sma_adaybefore = sum/20

diff = sma_adaybefore - sma_today

if diff > 0:
    print "Output of SMA20-slope analysis: BUY"
elif diff < 0:
    print "Output of SMA20-slope analysis: SELL"
else:
    print "SAME SMA20! SMA20-slope test is inconclusive"


with open('quotes-bollinger.json') as json_data_bollinger:
    data_bollinger = json.load(json_data_bollinger)

    #for changing format of data. Yeah taking the longer route only for testing purposes.
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

print di_bollinger