import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import tweepy
import time
import os

CONSUMER_KEY = os.environ.get('TWITTER_API_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_API_SECRET_KEY')
ACCESS_KEY = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def getProxies(inURL):
    page = requests.get(inURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    terms = soup.find_all('tr')
    IPs = []

    for x in range(len(terms)):  
        
        term = str(terms[x])        
        
        if '<tr><td>' in str(terms[x]):
            pos1 = term.find('d>') + 2
            pos2 = term.find('</td>')

            pos3 = term.find('</td><td>') + 9
            pos4 = term.find('</td><td>US<')
            
            IP = term[pos1:pos2]
            port = term[pos3:pos4]
            
            if '.' in IP and len(port) < 6:
                IPs.append(IP + ":" + port)

    return IPs 

proxyURL = "https://www.us-proxy.org/"
pxs = getProxies(proxyURL)

proxies = {
  'http': 'http://' + pxs[0],
  'http': 'http://' + pxs[1],
  'http': 'http://' + pxs[2],
  'http': 'http://' + pxs[3],
  'http': 'http://' + pxs[4],
  'http': 'http://' + pxs[5],
  'http': 'http://' + pxs[6],
  'http': 'http://' + pxs[7],
}

class stockPerf():
    def __init__(self, s, p):
        self.stock = s
        self.perf = p

    def setStock(self, s):
        self.stock = s

    def setPerf(self, p):
        self.perf = p

data = []
smas = ""
priceRatings = []
newsT = []
symbols = []
price = ""
change = ""
prevClose = ""
ps = ""
rsi = ""
earnings = ""
targetPrice = ""
perfWeek = ""
perfMonth = ""
perfQuarter = ""
perfYTD = ""
quarterlyRevGrowth = ""
epsGrowth = ""
debtEquity = ""
profitMargin = ""
dividend = ""
roa = ""
tg = ""
stockCounter = 0
c = 1
skip = False
sma20 = 0
sma50 = 0
sma200 = 0
pe = 0
forwardPE = 0
text = ""
perfWeekMax = -10000
allPerfs = []
c2 = []
maxSmas = []
earningsDates = []
profitMargins = []
text = ''
pegs = []
f52Low = ''
f52Lows = []
instut = ''
insOwn = []

def getTechnicals(inURL, sy):
    page = requests.get(inURL + sy)
    soup = BeautifulSoup(page.text, 'html.parser')
    technicals = soup.find_all('tr', {'class' : 'table-dark-row'})
    pts = soup.find_all('table', {'class' : 'fullview-ratings-outer'})
    news = soup.find_all('table', {'class': 'fullview-news-outer'})

    global data
    global smas
    global pes
    global priceRatings
    global ps
    global rsi
    global earnings
    global price
    global change
    global prevClose
    global targetPrice 
    global perfWeek
    global perfMonth
    global perfQuarter
    global perfYTD
    global quarterlyRevGrowth
    global profitMargin
    global dividend
    global roa
    global tg
    global skip
    global sma20
    global sma50
    global sma200
    global pe
    global forwardPE
    global perfWeekMax
    global allPerfs
    global c2
    global maxSmas
    global earningsDates
    global profitMargins
    global pegs
    global f52Low
    global f52Lows
    global instut
    global insOwn

    for t in range(len(technicals)):
        data.append(technicals[t].text.strip())

    for t in range(len(data)):
        if 'Price' in data[t]:
            price = data[t][data[t].find('Price') + 5 : ].strip()

        if 'Change' in data[t]:
            change = data[t][data[t].find('Change') + 6 : ].strip()

        if 'Prev Close' in data[t]:
            prevClose = data[t][data[t].find('Prev Close') + 10 : ].strip()

        if 'SMA' in data[t]:
            smas = (data[t][data[t].find('SMA') : data[t].find('Volume')])

        if 'P/E' in data[t]:
            if 'Index' in data[t]:
                pe = data[t][data[t].find('P/E') + 3 : data[t].find('EPS')].strip()

        if 'Forward P/E' in data[t]:
            forwardPE = data[t][data[t].find('Forward P/E') + 11 : data[t].find('EPS')].strip()

        if 'P/S' in data[t]:
            ps = data[t][data[t].find('P/S') + 3 : data[t].find('EPS') - 1]

        if 'RSI' in data[t]:
            rsi = data[t][data[t].find('(14)') + 4 : data[t].find('(14)') + 9]
        
        if 'Earnings' in data[t]:
            earnings = data[t][data[t].find('Earnings') + 8 : data[t].find('Earnings') + 18]
        
        if 'Target Price' in data[t]:
            targetPrice = data[t][data[t].find('Target Price') + 12 : data[t].find('Perf') - 1]

        if 'Perf Week' in data[t]:
            perfWeek = data[t][data[t].find('Week') + 4 : ]
        
        if 'Perf Month' in data[t]:
            perfMonth = data[t][data[t].find('Month') + 5 : ]

        if 'Perf Quarter' in data[t]:
            perfQuarter = data[t][data[t].find('Quarter') + 7 :]

        if 'Perf YTD' in data[t]:
            perfYTD = data[t][data[t].find('YTD') + 3 : ]
        
        if 'Sales Q/Q' in data[t]:
            quarterlyRevGrowth = data[t][data[t].find('Sales Q/Q') + 9 : data[t].find('%') + 1]
        
        if 'Profit Margin' in data[t]:
            profitMargin = data[t][data[t].find('Profit Margin') + 13: data[t].find('Profit Margin') + 19].strip()
        
        if 'Dividend' in data[t]:
            dividend = data[t][data[t].find('Dividend') + 10 : data[t].find('.') + 4]

        if 'ROA' in data[t]:
            roa = data[t][data[t].find('ROA') + 3 : data[t].find('ROA') + 9].strip()

        if 'ROE' in data[t]:
            roe = data[t][data[t].find('ROE') + 3 : data[t].find('ROE') + 9].strip()

        if 'EPS Q/Q' in data[t]:
            epsGrowth = data[t][data[t].find('EPS Q/Q') + 7 : data[t].find('%')]

        if 'Debt/Eq' in data[t]:
            debtEquity = data[t][data[t].find('Debt/Eq') + 7: data[t].find('Debt/Eq') + 12]

        if 'PEG' in data[t]:
            peg = data[t][data[t].find('PEG') + 3 : data[t].find('EPS') - 1]

        if '52W Low' in data[t]:
            f52Low = data[t][data[t].find('52W Low') + 7 : data[t].find('ATR') - 2].strip()

        if 'Inst Own' in data[t]:
            instut = data[t][data[t].find('Inst Own') + 8 : data[t].find('Short Float') - 2]

    #---------------------------------------------------------------------------------------------------
   
    for t in range(len(pts)):
        priceRatings.append(pts[t].text.strip())
    try:
        priceRatings = priceRatings[0].split('\n')
    except:
        priceRatings = []

    for x in range(len(news)):
        tg = news[x].text
    
    s = getSMAs()

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    for t in range(len(pts)):
        priceRatings.append(pts[t].text.strip())
    
    try:
        priceRatings = priceRatings[0].split('\n')
    except:
        priceRatings = []

    for x in range(len(news)):
        tg = news[x].text
    
    #-----------------------------------------------------------------------------------
    
    try:
        allPerfs.append(stockPerf(sy, float(perfWeek[:-1])))
        c2.append([sy, float(change[ : -1])])
        maxSmas.append([sy, float(sma20[: -1])])
    except:
        print('')

    if '-' not in profitMargin:
        profitMargins.append([sy, float(profitMargin[: -1])])

    if '-' not in earnings:
        earningsDates.append([sy, earnings])

    if '-' not in peg:
        pegs.append([sy, float(peg)])

    if '-' not in f52Low and len(f52Low) > 1:
        f52Lows.append([sy, float(f52Low)])

    if '-' not in instut and len(instut) > 1:
        insOwn.append([sy, float(instut)])

    #------------------------------------------------------------------------------------

def getSymbols(inURL, add):
    global stockCounter
    global c
    page = requests.get(inURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    symbs = soup.find_all('a', {'class' : 'screener-link-primary'})

    for x in range(len(symbs)):
        if '&amp;b=1' in str(symbs[x]):
            symbols.append(str(symbs[x])[str(symbs[x]).find('&amp;b=1') + 10 : str(symbs[x]).find('/a') - 1])
            stockCounter = stockCounter + 1

        if stockCounter % 20 == 0:
            c = c + 20
            getSymbols('https://finviz.com/screener.ashx?v=111' + addOn + '&r=' + str(c), addOn)
        
        if stockCounter >= 7600:
            break

    return symbols

def printStats(sy):
    
    global data
    global smas
    global pes
    global priceRatings
    global ps
    global rsi
    global earnings
    global price
    global change
    global prevClose
    global targetPrice 
    global perfWeek
    global perfMonth
    global perfQuarter
    global perfYTD
    global quarterlyRevGrowth
    global profitMargin
    global dividend
    global roa
    global tg
    global skip
    global pe
    global forwardPE
    global text
    global sma20
    global sma50
    global sma200
    
    cc = float(price) - float(prevClose)

    pfs = getPerfs()
    
    print('------------------------------------------------------------------------------------')
    
    skip = True
    
    print(sy)
    text += '\n' + sy
    
    print('Price: ' + price)
    text += '\n' + price

    if cc > 0:
        print('+' + str(cc)[0 : 4], change)
        text += '\n+' + str(cc)[0 : 4] + '  ' + change
    else:
        print(str(cc)[0 : 4], change)
        text += '\n' + str(cc)[0 : 4] + '  ' + change

    print('P/E: ' + pe + '  Forward P/E: ' + forwardPE)
    text += '\nP/E: ' + pe + '  Forward P/E: ' + forwardPE
    
    print('Profit Margin: ' + profitMargin)
    text += '\nProfit Margin: ' + profitMargin
    
    print('SMA 20: ' + sma20 + '  SMA 50: ' + sma50 +  '  SMA 200: ' + sma200)
    text += '\nSMA 20: ' + sma20 + '  SMA 50: ' + sma50 +  '  SMA 200: ' + sma200
    
    print('Perf Week ' + pfs[0] + '  Perf Month: ' + pfs[1] + '  Perf Quarter: ' + pfs[2] + '  Perf YTD: ' + pfs[3])
    text += '\nPerf Week ' + pfs[0] + '  Perf Month: ' + pfs[1] + '  Perf Quarter: ' + pfs[2] + '  Perf YTD: ' + pfs[3]
    
    if '-' not in earnings:
        print('Earnings Date: ' + earnings)
        text += '\nEarnings Date: ' + earnings
    
    if '-' not in quarterlyRevGrowth:
        print('Quarterly Revenue Growth: ' + quarterlyRevGrowth)
        text += '\nQuarterly Revenue Growth: ' + quarterlyRevGrowth
    
    print('RSI: ' + rsi)
    text += '\nRSI: ' + rsi
    
    if '-' not in dividend:
        print('Dividend ' + dividend)
        text += '\nDividend ' + dividend + '\n'
    
    text += '\n'

def bubbleSort(subList): 
    
    l = len(subList) 

    for i in range(0, l): 
        
        for j in range(0, l-i-1): 
            
            if (subList[j][1] > subList[j + 1][1]): 
                tempo = subList[j] 
                subList[j]= subList[j + 1] 
                subList[j + 1]= tempo 

    return subList     

def convertNum(stng):
    s = ''

    if len(stng) > 20:
        return 0

    for x in range(len(stng) - 1):
        if stng[x] == '-' and stng[x + 1] != '-':
            s += stng[x]
        
        elif stng[x] == '.':
            s += stng[x]

        elif stng[x] != ',' and stng[x] != "'" and stng[x] != '"' and (not stng[x].isalpha()) and stng[x] != ':' and stng[x].isdigit() and stng[x + 1] != '"':
            s += stng[x]

    if len(s) > 0 and len(s) < 10:
        try:
            return float(s)
        except:
            return 0

    return 0

def loop():
    
    global dat
    global smas
    global pes
    global priceRatings
    global ps
    global rsi
    global earnings
    global price
    global change
    global prevClose
    global targetPrice 
    global perfWeek
    global perfMonth
    global perfQuarter
    global perfYTD
    global quarterlyRevGrowth
    global profitMargin
    global dividend
    global roa
    global tg
    global skip
    global addOn
    global sma20
    global sma50
    global sma200
    global pe 
    global forwardPE
    
    ss =  getSymbols('https://finviz.com/screener.ashx?v=111' + addOn + '&r=' + str(c), addOn)

    for x in range(len(ss)):
        getTechnicals('https://finviz.com/quote.ashx?t=', ss[x])

        if skip == True:
            print('\n')
        
        data = []
        smas = ""
        pes = []
        priceRatings = []
        newsT = []
        symbols = []
        price = ""
        change = ""
        prevClose = ""
        ps = ""
        rsi = ""
        earnings = ""
        targetPrice = ""
        perfWeek = ""
        perfMonth = ""
        perfQuarter = ""
        perfYTD = ""
        quarterlyRevGrowth = ""
        profitMargin = ""
        dividend = ""
        roa = ""
        tg = ""
        skip = False
        sma20 = 0
        sma50 = 0
        sma200 = 0
        pe = 0
        forwardPE = 0

def getSMAs():
    global smas
    global sma20
    global sma50
    global sma200

    sma20 = smas[smas.find('SMA20')  + 5 : smas.find("%") + 1]
    smas = smas[smas.find("%") + 1 : ]
    sma50 = smas[smas.find('SMA50') + 5: smas.find("%") + 1]
    smas = smas[smas.find("%") + 1 : ]
    sma200 = smas[smas.find('SMA200') + 6: smas.find("%") + 1]
  
    ss = [sma20, sma50, sma200]
    return ss

def getPerfs():
    perfs = [perfWeek, perfMonth, perfQuarter, perfYTD]
    return perfs

def getTop5PerfWeek():
    
    global allPerfs
    global text

    loop()
    
    top5PerfWeek = []
    index = 0

    for x in range(5):
        
        maxPerf = allPerfs[0].perf

        for y in range(len(allPerfs)):
            if allPerfs[y].perf > maxPerf:
                maxPerf = allPerfs[y].perf
                index = y

        top5PerfWeek.append(stockPerf(allPerfs[index].stock, maxPerf))
        del allPerfs[index]

    print('Top Gainers for the Week: ')
    text += 'Top Gainers for the Week: '
    text += '\n'

    for x in range(len(top5PerfWeek)):
        print('$' + str(top5PerfWeek[x].stock), '+' + str(top5PerfWeek[x].perf) + '%')
        text += '$' + str(top5PerfWeek[x].stock) + ' +' + str(top5PerfWeek[x].perf) + '%'
        text += '\n'

def getWorst5PerfWeek():
        
    global allPerfs
    global text

    loop()
    
    worst5PerfWeek = []
    index = 0

    for x in range(5):
        
        minPerf = allPerfs[0].perf

        for y in range(len(allPerfs)):
            if allPerfs[y].perf < minPerf:
                minPerf = allPerfs[y].perf
                index = y

        worst5PerfWeek.append(stockPerf(allPerfs[index].stock, minPerf))
        del allPerfs[index]

    print('Worst Performers for the Week: ')
    text += 'Worst Performers for the Week: '
    text += '\n'

    for x in range(len(worst5PerfWeek)):
        print('$' + str(worst5PerfWeek[x].stock), '' + str(worst5PerfWeek[x].perf) + '%')
        text += '$' + str(worst5PerfWeek[x].stock) + ' ' + str(worst5PerfWeek[x].perf) + '%'
        text += '\n'

def getBiggestMoversAfterHours():
    global text
    
    page = requests.get('https://www.marketwatch.com/tools/screener/after-hours')
    soup = BeautifulSoup(page.text, 'html.parser')
    rawSymbols = soup.find_all('a', {'class' : 'link'})
    rawPercentChanges = soup.find_all('li', {'class' : 'content__item value ignore-color'})
    percentChanges = []
    pchanges2 = []
    symbols = []

    for x in range(len(rawSymbols)):
        s = str(rawSymbols[x])
        ss = s[s.find('">') + 2 : s.find('</')]

        if 'Home' not in ss and 'Tools' not in ss and 'Help' not in ss and len(ss) <= 4 and len(ss) > 0:
            symbols.append(ss)

    for x in range(len(rawPercentChanges)):
        s = str(rawPercentChanges[x])
        ss = s[s.find('>') + 1 : s.find('</') - 1]
        percentChanges.append(ss)
        pchanges2.append(ss)
    
    stockChange = []

    for x in range(len(symbols)):
        stockChange.append([symbols[x], percentChanges[x]])

    top3Pos = stockChange[0 : 3]
    top3Neg = stockChange[10 : 13]

    print('Top Movers After Hours: ' + '\n')
    text += 'Top Movers After Hours: ' + '\n\n'

    for x in range(len(top3Pos)):
        print('$' + top3Pos[x][0], '+' + str(top3Pos[x][1]) + '%')
        text += '$' + top3Pos[x][0] + ' +' + str(top3Pos[x][1]) + '%' + '\n'
    
    print() 
    text += '\n'

    for x in range(len(top3Neg)):
        print('$' + top3Neg[x][0], str(top3Neg[x][1]) + '%')
        text += '$' + top3Neg[x][0] + ' ' + str(top3Neg[x][1]) + '%' + '\n'

def getFutures():
    global text
    
    page = requests.get('https://money.cnn.com/data/premarket/')
    soup = BeautifulSoup(page.text, 'html.parser')
    rawChanges = soup.find_all('span', {'class' : 'posData'})
    rawTime = str(soup.find_all('div', {'class' : 'wsod_fRight wsod_disclaimer'}))
    rawPercentChange = soup.find_all('span', {'class' : 'posChangePct'})
    time = rawTime[rawTime.find('Data') : rawTime.find('</')]

    changes = []
    percentChanges = []

    for x in range(3, 6):
        s = str(rawPercentChange[x])
        percentChanges.append(s[s.find('>') + 1:  s.find('</')])

    for x in range(len(rawChanges)):
        s = str(rawChanges[x])
        changes.append(s[s.find('posData">') + 9 : s.find('</')])

    print('U.S. Stock Futures' + '\n')
    text += 'U.S. Stock Futures' + '\n\n'
    
    print('S&P',  changes[0], '/ ' + percentChanges[0])
    text += 'S&P' + ' ' + changes[0] + ' / ' + percentChanges[0] + '\n'

    print('Nasdaq',  changes[1], '/ ' + percentChanges[1])
    text += 'Nasdaq' + ' ' + changes[1] + ' / ' + percentChanges[1] + '\n'

    print('Dow',  changes[2], '/ ' + percentChanges[2])
    text += 'Dow' + ' ' + changes[2] + ' / ' + percentChanges[2] + '\n'

    print('\n' + time)
    text += '\n\n' + time

def getBiggestMoversToday():
    global text
    global c2

    loop()

    for x in range(len(c2)):
        for y in range(len(c2) - 1):
            if c2[y][1] < c2[y + 1][1]:
                temp = c2[y]
                c2[y] = c2[y + 1]
                c2[y + 1] = temp

    print(c2)

    print('Biggest Movers Today: ' + '\n')
    text += 'Biggest Movers Today: ' + '\n\n'

    for x in range(3):
        print('$' + c2[x][0], '+' + str(c2[x][1]) + '%')
        text += '$' + c2[x][0] + ' +' + str(c2[x][1]) + '%' + '\n'

    print()
    text += '\n'

    for x in range(len(c2) - 1, len(c2) - 4, -1):
        print('$' + c2[x][0], str(c2[x][1]) + '%')
        text += '$' + c2[x][0] + ' ' + str(c2[x][1]) + '%' + '\n'

def getPutCallRatio():
    global text 
    global symbols
    global proxies

    page = requests.get('https://ycharts.com/indicators/cboe_spx_put_call_ratio', proxies=proxies)
    soup = str(BeautifulSoup(page.text, 'html.parser'))
    s = soup[soup.find('SPX Put/Call Ratio is at a current level') : soup.find('SPX Put/Call Ratio is at a current level') + 176]
    ss = s[0 : s.find('day') + 3]
    change = s[s.find('change of ') + 10 : s.find('change of') + 16]
    
    print(str(ss) + '. This is a change of', change)
    text += str(ss) + '. This is a change of ' + str(change)

def getMaxSma20():
    global maxSmas
    global text

    loop()

    sortedList = bubbleSort(maxSmas)
    topPicks = []

    for x in range(len(sortedList)):
        if sortedList[x][1] > 4:
            topPicks.append(sortedList[x])

    t5 = topPicks[0 : 5]
    
    print('Stocks with great setup patterns: ' + '\n')
    text += 'Stocks with great setup patterns: ' + '\n\n'

    for x in range(len(t5)):
        print('$' + t5[x][0], '+' + str(t5[x][1]) + '% over SMA20')
        text += '$' + t5[x][0] + ' +' + str(t5[x][1]) + '% over SMA20' + '\n'

def getUpcomingEarnings():
    global text
    global earningsDates

    loop()
    upcomingEarnings = []

    for x in range(len(earningsDates)):
        if 'Jan 11' in earningsDates[x][1] or 'Jan 14' in earningsDates[x][1] or 'Jan 15' in earningsDates[x][1] or 'Jan 16' in earningsDates[x][1] or 'Jan 17' in earningsDates[x][1] or 'Jan 18' in earningsDates[x][1]:
            upcomingEarnings.append(earningsDates[x])

    print(upcomingEarnings)
    print()

    for x in range(len(upcomingEarnings)):
        for y in range(len(upcomingEarnings) - 1):
            s = upcomingEarnings[y][1]
            s2 = upcomingEarnings[y + 1][1]
            currDate = s[s.find('Jan') + 4 : s.find('Jan') + 6]
            nextDate = s2[s2.find('Jan') + 4 : s2.find('Jan') + 6]

            if currDate > nextDate:
                temp = upcomingEarnings[y]
                upcomingEarnings[y] = upcomingEarnings[y + 1]
                upcomingEarnings[y + 1] = temp

    print('Upcoming Earnings Reports:' + '\n')
    text += 'Upcoming Earnings Reports: ' + '\n\n'

    for x in range(6):
        print('$' + upcomingEarnings[x][0], upcomingEarnings[x][1])
        text += '$' + upcomingEarnings[x][0] + ' ' + upcomingEarnings[x][1] + '\n'

def industryComparisons(s):
    global text
    global symbols

    loop()

    if s == 'net margin':
        margins = []

        for x in range(len(symbols)):
            page = requests.get('https://csimarket.com/stocks/Profitability.php?code=' + symbols[x])
            soup = str(BeautifulSoup(page.text, 'html.parser'))
            rawNetMargin = soup[soup.find('"period": "Net Margin"') + 25 : soup.find('"period": "Net Margin"') + 100].strip()
            netMargin = rawNetMargin[rawNetMargin.find('visits') + 9 : rawNetMargin.find(',') - 1].strip()
            n = rawNetMargin[rawNetMargin.find(',') + 1 : ]
            industryNetMargin = n[n.find('visits1') + 10 : n.find(',')].strip()

            if len(netMargin) < 10 and len(industryNetMargin) < 10 and float(netMargin) > float(industryNetMargin):
                margins.append([symbols[x], netMargin, industryNetMargin])
            
        maxChange = float(margins[0][1]) - float(margins[0][2])
        index = 0

        for x in range(len(margins)):
            if float(margins[x][1]) - float(margins[x][2]) > maxChange:
                maxChange = float(margins[x][1]) - float(margins[x][2])
                index = x

        print('$' + margins[index][0] + ' has a net margin of ' + margins[index][1] + '%, compared to its industry average of ' + margins[index][2] + '%')
        text += '$' + margins[index][0] + ' has a net margin of ' + margins[index][1] + '%, compared to its industry average of ' + margins[index][2] + '%'
    
    elif s == 'roe':
        roes = []

        for x in range(len(symbols)):
            page = requests.get('https://csimarket.com/stocks/' + symbols[x] + '-Management-Effectiveness-Comparisons.html')
            soup = str(BeautifulSoup(page.text, 'html.parser'))

            rawRoe = soup[soup.find('"period": "ROE"') + 25 : soup.find('"period": "ROE"') + 100]
            roe = rawRoe[rawRoe.find(':') + 2 : rawRoe.find(',') - 1]
            r = rawRoe[rawRoe.find(',') + 1 : ]
            industryROE = r[r.find(':') + 2 : r.find(',') - 1]

            if len(roe) < 10 and len(industryROE) < 10 and float(roe) > float(industryROE):
                roes.append([symbols[x], float(roe), float(industryROE)])
 
        for x in range(len(roes)):
            for y in range(len(roes) - 1):
                if ((roes[y][1]) - roes[y][2]) < (roes[y + 1][1] - roes[y + 1][2]):
                    temp = roes[y]
                    roes[y] = roes[y + 1]
                    roes[y + 1] = temp
        
        print('Stocks with the highest ROE relative to their industry average: ' + '\n')
        text += 'Stocks with the highest ROE relative to their industry average: ' + '\n\n'

        for x in range(5):
            print('$' + roes[x][0] + ' ROE: ' + str(roes[x][1]) + '%' + '  Industry Average: ' + str(roes[x][2]) + '%')
            text += '$' + roes[x][0] + ' ROE: ' + str(roes[x][1]) + '%' + '  Industry Average: ' + str(roes[x][2]) + '%' + '\n'
        
def growthEstimates():
    global text 
    global symbols

    loop()
    revGrowth = []

    for x in range(len(symbols)):
        page = requests.get('https://finance.yahoo.com/quote/' + symbols[x] + '/analysis')
        soup = str(BeautifulSoup(page.text, 'html.parser'))
        currQtr = soup[soup.find('data-reactid="402">') + 19 : soup.find('</td><td class="Ta(end) Py(10px)" data-reactid="403"') - 1]
        nextQtr = soup[soup.find('data-reactid="409">') + 19 : soup.find('</td><td class="Ta(end) Py(10px)" data-reactid="410">') - 1]
        currYear = soup[soup.find('data-reactid="416">') + 19 : soup.find('</td><td class="Ta(end) Py(10px)" data-reactid="417"') - 1]
        nextYear = soup[soup.find('data-reactid="423">') + 19 : soup.find('</td><td class="Ta(end) Py(10px)" data-reactid="424"') - 1]
        salesGrowthCurrQuarter = soup[soup.find('data-reactid="171">') + 19 : soup.find('</span></td><td class="Ta(end)" data-reactid="172">') - 1]
        salesGrowthNextQuarter = soup[soup.find('data-reactid="173">') + 19 : soup.find('</span></td><td class="Ta(end)" data-reactid="174">') - 1]
        
        if len(salesGrowthCurrQuarter) < 10 and 'N/A' not in salesGrowthCurrQuarter and 'N/' not in salesGrowthCurrQuarter:
            revGrowth.append([symbols[x], float(salesGrowthCurrQuarter)])

    bubbleSort(revGrowth)
    revGrowth.reverse()
    
    print('Stocks with the highest revenue growth estimates for the current qtr (Dec 2018):' + '\n')
    text += 'Stocks with the highest revenue growth estimates for the current qtr (Dec 2018):' + '\n\n'
    
    for x in range(5):
        print('$' + revGrowth[x][0] + ' ' + str(revGrowth[x][1]) + '%')
        text += '$' + revGrowth[x][0] + ' ' + str(revGrowth[x][1]) + '%' + '\n'
    
def lowestPEGs():
    global text
    global pegs

    loop()

    bubbleSort(pegs)

    print('Stocks with exceptionally cheap PEG ratios: ' + '\n')
    text += 'Stocks with exceptionally cheap PEG ratios: ' + '\n\n'

    for x in range(5):
        print('$' + pegs[x][0] + ' ' + str(pegs[x][1]))
        text += '$' + pegs[x][0] + ' ' + str(pegs[x][1]) + '\n'

def rebound52WeekLow():
    global text
    global f52Lows
    
    loop()

    bubbleSort(f52Lows)
    f52Lows.reverse()

    print('Stocks that have rebounded the most off their 52 week lows: ' + '\n')
    text += 'Stocks that have rebounded the most off their 52 week lows: ' + '\n\n'

    for x in range(5):
        print('$' + f52Lows[x][0] + ' +' + str(f52Lows[x][1]) + '%')
        text += '$' + f52Lows[x][0] + ' +' + str(f52Lows[x][1]) + '%' + '\n'
    
def revPerEmployee():
    global text
    global symbols

    loop()

    revs = []

    for x in range(len(symbols)):
        page = requests.get('https://csimarket.com/stocks/' + symbols[x] + '-Efficiency-Comparisons.html')
        soup = str(BeautifulSoup(page.text, 'html.parser'))
        rawRev = soup[soup.find('<td class="gorub s ddd">') + 25 : soup.find('<td class="gorub">') - 20].strip()
        rawIndRev = soup[soup.find('<td class="gorub">') + 20 : soup.find('<td class="gorub ddd">') - 20].strip()
        
        if len(rawRev) < 20 and len(rawRev) > 1:
            
            rev = ''
            indRev = ''
            for y in range(len(rawRev)):
                if rawRev[y] != ',':
                    rev += rawRev[y]

            for z in range(len(rawIndRev)):
                if rawIndRev[z] != ',':
                    indRev += rawIndRev[z]

            
            if float(rev) > float(indRev):
                revs.append([symbols[x], float(rev), float(indRev), rawRev, rawIndRev])

    for x in range(len(revs)):
        for y in range(len(revs) - 1):
            if revs[y][1] - revs[y][2] < revs[y + 1][1] - revs[y + 1][2]:
                temp = revs[y]
                revs[y] = revs[y + 1]
                revs[y + 1] = temp
    
    print('Companies with the highest revenue per employee relative to their industry average: ' + '\n')
    text += 'Companies with the highest revenue per employee relative to their industry average: ' + '\n\n'

    for x in range(3):
        print('$' + revs[x][0] + ' Rev/Employee: $' + revs[x][3] + '  Industry Average: $' + revs[x][4])
        text += '$' + revs[x][0] + ' Rev/Employee: $' + revs[x][3] + '  Industry Average: $' + revs[x][4] + '\n'

def qtrEpsGrowth():
    global text
    global symbols
    
    loop()

    eps = []
    
    for x in range(len(symbols)):
        page = requests.get('https://finance.yahoo.com/quote/' + symbols[x] + '/analysis?p=BA&.tsrc=fin-srch')
        soup = str(BeautifulSoup(page.text, 'html.parser'))
        avgEstimate = soup[soup.find('data-reactid="46">') + 18 : soup.find('data-reactid="47">') - 32]
        yearAgoEps = soup[soup.find('data-reactid="79">') + 18 : soup.find('data-reactid="80">') - 32]
        
        monthYear = soup[soup.find('>Current Qtr.</span><!-- react-text: 13 --> (<!-- /react-text --><span data-reactid="14">') : soup.find(')<!-- /react-text --></span></th><th class="Fw(400) W(20%) Fz(xs) C($c-fuji-grey-j) Ta(end)" data-reactid="16">')]
        mY = monthYear[monthYear.find('id="14">') + 8: monthYear.find('id="14">') + 11] + ' ' + monthYear[-4 : ]    

        if 'N/A' not in avgEstimate and 'N/A' not in yearAgoEps and len(avgEstimate) < 10 and len(yearAgoEps) < 10 and len(avgEstimate) > 0 and len(yearAgoEps) > 0: #and float(avgEstimate) > float(yearAgoEps):
            avg = convertNum(avgEstimate)
            yae = convertNum(yearAgoEps)

            if avg > yae:
                ch = 0
                if yae != 0:
                    ch = ((avg - yae) / yae) * 100
                eps.append([symbols[x], avg, yae, ch, mY])

    for x in range(len(eps)):
        for y in range(len(eps) - 1):
            if eps[y][3] < eps[y + 1][3]:
                temp = eps[y]
                eps[y] = eps[y + 1]
                eps[y + 1] = temp
          
    print('Analysts for $' + eps[0][0] + ' have an average EPS estimate of ' + str(eps[0][1]) + ' for the current quarter (' + eps[0][4] + '). This is a change of +' + str(eps[0][3])[0 : 4] + '% from last year''s EPS of ' + str(eps[0][2]) + '.') 
    text += 'Analysts for $' + eps[0][0] + ' have an average EPS estimate of ' + str(eps[0][1]) + ' for the current quarter (' + eps[0][4] + '). This is a change of +' + str(eps[0][3])[0 : 4] + '% from last year''s EPS of ' + str(eps[0][2]) + '.'

def insOwnership():
    global text
    global insOwn

    loop()

    bubbleSort(insOwn)
    insOwn.reverse()

    print('Stocks with the largest institutional ownership: ' + '\n')
    text += 'Stocks with the largest institutional ownership: ' + '\n\n'

    for x in range(5):
        print('$' + insOwn[x][0] + ' ' + str(insOwn[x][1]) + '%')
        text += '$' + insOwn[x][0] + ' ' + str(insOwn[x][1]) + '%' + '\n'

def getScores():
    global text  

    symbols =  getSymbols('https://finviz.com/screener.ashx?v=111' + addOn + '&r=' + str(c), addOn)

    stSurprise = []

    for x in range(len(symbols)):
        page = requests.get('https://finance.yahoo.com/quote/' + symbols[x] + '/analysis')
        soup2 = BeautifulSoup(page.text, 'html.parser')
        soup = str(BeautifulSoup(page.text, 'html.parser'))

        surprises = []
        revenueGrowth = []
        earningsGrowth = []
        
        surpriseSum = 0
        revSum = 0

        surprisesPositive = 0
        revPositive = 0

        earningsSum = 0
        earningsPositive = 0

        pegWeight = 40
        forPeWeight = 10
        revGrowthWeight = 8
        earningsGrowthWeight = 6
        surprisesWeight = 0.5
        operatingMarginWeight = 3
        profitMarginWeight = 3

        stats = requests.get('https://finance.yahoo.com/quote/' + symbols[x] + '/key-statistics')
        rawStats = str(BeautifulSoup(stats.text, 'html.parser'))

        rawYearChange = rawStats[rawStats.find('52WeekChange":') + 20 : rawStats.find(',"morningStarRiskRating')]
        
        ####ADJUSTED
        yearChange = 2 * convertNum(rawYearChange[rawYearChange.find('fmt') + 6 : rawYearChange.find('%')]) 

        ####ADJUSTED
        pegRatio = pegWeight * (5 - convertNum(rawStats[rawStats.find('data-reactid="47">') + 18 : rawStats.find('</td></tr><tr data-reactid="48"')]))

        if pegRatio >= pegWeight * 5 or pegRatio < 0:
            pegRatio = 0

        rawPMargin = rawStats[rawStats.find('profitMargins":{') : rawStats.find('"enterpriseToEbitda":{')]
        
        ####ADJUSTED
        pMargin = profitMarginWeight * convertNum(rawPMargin[rawPMargin.find('fmt":"') + 5 : rawPMargin.find('%')])
        
        rawOpMargin = rawStats[rawStats.find('operatingMargins":{') : rawStats.find('"ebitda":{')]
        
        ####ADJUSTED
        operMargin = operatingMarginWeight * convertNum(rawOpMargin[rawOpMargin.find('fmt":"') + 5 : rawOpMargin.find('%')])

        rawROE = rawStats[rawStats.find('returnOnEquity":{') : rawStats.find('"targetHighPrice":{')]
        
        ####ADJUSTED
        returnOnEq = 2 * convertNum(rawROE[rawROE.find('fmt":"') + 5 : rawROE.find('%')])
        
        rawForwardPE = rawStats[rawStats.find('forwardPE":{') : rawStats.find('"maxAge":1,"lastCapGain')]
        
        ####ADJUSTED
        forPe = forPeWeight * (100 - convertNum(rawForwardPE[rawForwardPE.find('fmt":"') + 5 : rawROE.find('%')]))

        if forPe >= forPeWeight * 100 or forPe < 0:
            forPe = 0
        
        rawRevGrowth = soup2.find_all('tr', {'class' : 'BdT Bdc($c-fuji-grey-c)'})
        rawEarnGrowth = soup2.find_all('tr', {'class' : 'BdT Bdc($c-fuji-grey-c)'})

        if len(rawRevGrowth) > 0:   
            s = str(rawRevGrowth[10])

            for y in range(4):
                revenueGrowth.append(convertNum(s[s.find('data-reactid="17') + 65 : s.find('%')]))
                s = s[s.find('%') + 1 : ]

            for z in range(len(revenueGrowth)):
                if revenueGrowth[z] > 0:
                    revPositive += 1

                ####ADJUSTED
                revSum += revGrowthWeight * revenueGrowth[z]
                    

        if len(rawEarnGrowth) > 0:
            for n in range(len(rawEarnGrowth) - 6, len(rawEarnGrowth)):
                s = str(rawEarnGrowth[n])
                earningsGrowth.append(convertNum(s[s.find('td class="Ta(end) Py(10px)" data-reactid') + 47 : s.find('%')]))

            for m in range(len(earningsGrowth)):
                if earningsGrowth[m] > 0:
                    earningsPositive += 1 

                ####ADJUSTED
                earningsSum += earningsGrowthWeight * earningsGrowth[m]
                      

        for y in range(4):
            if len(soup[soup.find('surprisePercent":{') + 37 : soup.find(',"quarter":{') - 3]) < 100:
                surprises.append(convertNum(soup[soup.find('surprisePercent":{') + 35 : soup.find(',"quarter":{') - 3]))
                soup = soup[soup.find(',"quarter":{') + 12 : ]

        if len(surprises) > 0:
            for z in range(len(surprises)):
                if surprises[z] > 0:
                    surprisesPositive += 1

                ####ADJUSTED
                surpriseSum += surprisesWeight * surprises[z]
                    
        
        if surprisesPositive == 4 and revPositive == 4 and earningsPositive == 6 and pMargin > 0:
            stSurprise.append([symbols[x], (surpriseSum + revSum + earningsSum + yearChange + forPe + returnOnEq + pMargin + operMargin + pegRatio) / 20])


        avg = (surpriseSum + revSum + earningsSum + yearChange + forPe + returnOnEq + pMargin + operMargin + pegRatio) / 20
        
        #if avg >= 90:
            #print(symbols[x], avg)
            #print()

        #if forPe != 0:
            #print(symbols[x], '\nRevenue Growth:', revenueGrowth, '\nSurprises:', surprises, '\nEarnings Growth:', earningsGrowth, '\nYear change:', yearChange, '\nForward PE:', forPe, '\nPEG:', pegRatio, '\nProfit Margin:', pMargin, '\nOperating Margin:', operMargin, '\nROE:', returnOnEq, '\nAverage:' , (surpriseSum + revSum + earningsSum + yearChange + forPe + returnOnEq + pMargin + operMargin + pegRatio) / 20)
            #print()

    bubbleSort(stSurprise)
    stSurprise.reverse()
    
    print(stSurprise[0 : 50])



mA = '&s=ta_mostactive'
tG = '&s=ta_topgainers'
tL = '&s=ta_toplosers'
mV = '&s=ta_mostvolatile'
oB = '&s=ta_overbought'
oS = '&s=ta_oversold'
addOn = ''

#getBiggestMoversAfterHours()
#getFutures()
#getTop5PerfWeek()
#getWorst5PerfWeek()
#getBiggestMoversToday()
#getPutCallRatio()

#getMaxSma20()
#getUpcomingEarnings()

#industryComparisons('roe')
#growthEstimates()

#lowestPEGs()
#rebound52WeekLow()
#revPerEmployee()
#qtrEpsGrowth()

#insOwnership()
getScores()
print('\n' + text)

#api.update_status(text)
