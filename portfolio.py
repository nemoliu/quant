import pandas as pd
import pandas_datareader.data as web
from risk_party import get_weights
import datetime
from datetime import date
from dateutil import relativedelta
from collections import defaultdict

def portfolio(ticker, start_date, end_date):
    prices = pd.DataFrame([web.DataReader(t,
                                      'yahoo',
                                      start_date,
                                      end_date).loc[:, 'Adj Close']
                       for t in [ticker]],
                      index=[ticker]).T.asfreq('B').ffill()
    return prices[ticker].values[-1]-prices[ticker].values[0], prices[ticker].values[0]


tickers = ['TLT', 'SSO', 'QLD']
dates = []
t_weights = defaultdict(list)

years = ['200%s'%i for i in range(8,10)]+['20%s'%i for i in range(10,20)]
monthes = ["0%s"%x for x in range(1,10)]+["%s"%x for x in range(10,13)]

for y in years:
    for m in monthes:
        dates.append("%s-%s-01" % (y,m))

for d in dates:
    cur_date = date.fromisoformat(d)
    t = relativedelta.relativedelta(years=-1)
    start_date = datetime.datetime((cur_date+t).year, (cur_date+t).month, (cur_date+t).day)
    end_date = datetime.datetime(cur_date.year, cur_date.month, cur_date.day)
    # print(start_date, end_date)
    weights = get_weights(tickers, start_date, end_date)
    for w, t in zip(weights, tickers):
        t_weights[t].append((end_date,w))

res = defaultdict(list)
for k,v in t_weights.items():
    i=0;
    j=i+1
    while j<len(v):
        p, price = portfolio(k, v[i][0], v[j][0])
        print(k, v[j][0], "%.2f"%p, "%.2f"%v[i][1])
        res[v[j][0]].append({'name':k, 'weight':"%.2f"%v[i][1], 'price': price, 'portf':"%.2f"%p})
        i+=1;
        j+=1;


keys = res.keys()
sorted(list(keys))
for k in keys:
    numerator = 0
    denominator = 1
    for stock in res[k]:
        numerator += float(stock['portf'])+float(stock['price'])*float(stock['weight'])
        denominator += float(stock['price'])*float(stock['weight'])

    print(k, "%.2f"%(numerator/denominator-1))
