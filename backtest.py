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


    print "Price minimas are: " + str(prices_minimas)
    print "MACD minimas are: " + str(macd_minimas)

    buy_con = []
    sel_con = []

    macd_con_sell = True
    macd_con_buy = True


    for amin in range(len(prices_minimas)):
        try:
            if prices_minimas[amin] < prices_minimas[amin + 1]:
                pass
            else:
                buy_con.append(0)
                print "Price analysis failed for Buy condition."
                macd_con_buy = False
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
                macd_con_buy = False
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
                macd_con_sell = False
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
                macd_con_sell = False
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
            macd_con_buy = False
            print "You must SELL as per line-cross analysis."
        if cross_list[0] == "cross_macd_now_high":
            macd_con_sell = False
            print "You must BUY as per line-cross analysis."
    elif len(cross_list) > 1:
        print "More than one cross. We will figure it out soon! :P"
    else:
        pass


    if macd_con_buy:
        results.append({"backtest_date": this_date, "test_name": "MACD", "result": "BUY", "operate_on": this_date, "price": price_this_date})
    if macd_con_sell:
        results.append({"backtest_date": this_date, "test_name": "MACD", "result": "SELL", "operate_on": this_date, "price": price_this_date})

print results

ofile  = open('macd_results.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
for aresult in results:
    row_list = []
    row_list.append(aresult["backtest_date"])
    row_list.append(aresult["price"])
    row_list.append(aresult["result"])
    row_list.append(aresult["operate_on"])
    row_list.append(aresult["test_name"])
    writer.writerow(row_list)

ofile.close()