import json
import csv

with open('quotes.json') as json_data:
    data = json.load(json_data)
    dates = []
    for agroup in data:
        for thedate in agroup.keys():
            dates.append(thedate)
    #get ordered dates
    dates = sorted(dates, reverse=True)

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

num_day = 1760

#the D-line analysis
print "Checking D-Line Analysis..."

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