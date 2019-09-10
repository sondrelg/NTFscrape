import bs4 as bs
import requests

def news(tickers, element = 1, exchange = 0):
    """To download stock news, please specify ticker of the stock, 
    which exchange it belongs to, and which element you wish to receive. 
    element = 1 returns the most recent news-listing."""
    #OSE 
    if exchange == 0:
        a = "http://www.netfonds.no/quotes/releases.php?paper="
        b = "&days=&location=paper&exchange=OSE"
    #Axess
    elif exchange == 1:
        a = "http://www.netfonds.no/quotes/releases.php?paper="
        b = "&days=&location=paper&exchange=OAX"        
    else:
        print("Please specify exchange = 0 for OSE, or exchange = 1 for Axess.")
    news = []
    for ticker in tickers: 
        try:
            resp = requests.get(a+ticker+b)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            table = soup.find('table', {'class': 'qbox releases'})
            new_entry = table.findAll('tr')[element].text
            news.append(new_entry)
        except:
            print("\nCould not collect news for {}.\n".format(ticker))
            pass
    return(news)
    print('\n')


def mcap(tickers, exchange = 0):
    """The function requires one or several tickers in list format. Please specify 'exchange = 1' to receive Axess-tickers. Function returns OSE tickers by default."""
    if exchange == 0:
        a = "http://www.netfonds.no/quotes/about.php?paper="
        b = ".OSE"
    elif exchange == 1:
        a = "http://www.netfonds.no/quotes/about.php?paper="
        b = ".OAX"
    else:
        print("Valid values for exchange includes 0 for OSE and 1 for Axess.")
        exit
    mcaps = []
    i = 0
    for ticker in tickers:
        try:
            resp = requests.get(a+ticker+b)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            table = soup.find('table', {'class': 'mbox'})
            new_entry_mcap = table.findAll('tr')[-5].text
            if new_entry_mcap[1] == "M":
                mcaps.append(new_entry_mcap + ticker)
                i += 1
            else:
                resp = requests.get(a+ticker+b)
                soup = bs.BeautifulSoup(resp.text, 'lxml')
                table = soup.find('table', {'class': 'mbox'})
                new_entry_mcap = table.findAll('tr')[-6].text
                if new_entry_mcap[1] == "M":
                    mcaps.append(new_entry_mcap + ticker)
                    i += 1
                else:
                    print("Unexpected error getting market cap for {}".format(ticker))
                    pass
        except:
            print("Could not get data for {}.".format(ticker))
            pass        
    #Remove OBX-elements, as these do not have mcaps
    i = 0
    for ticker, string in zip(tickers, mcaps):
        if "OBX" in ticker:
            tickers.pop(i)
        if "OBX" in string:
            mcaps.pop(i)
        i+=1
    #Slice away "Markedsverdi"
    for x in range(0,len(mcaps)):    
        mcaps[x] = mcaps[x][14:]
    #Slice out the market cap number
    mcaps_revised = []
    i = 0
    for a,b in zip(tickers, mcaps):
        length = len(a)+1
        mcaps_revised.append(mcaps[i][:-length])
        i += 1
    i = 0
    #Remove Whitespace and make INT
    for a in mcaps_revised:
        mcaps_revised[i] = int(a.replace(" ",""))
        i+=1
    return(mcaps_revised)


def get_tickers(exchange=0):
    """Please specify 'exchange = 1' to receive Axess-tickers. Function returns OSE tickers by default."""
    if exchange == 0:
        url = "http://www.netfonds.no/quotes/kurs.php"
    elif exchange == 1:
        url = "http://www.netfonds.no/quotes/kurs.php?exchange=OAX"
    else:
        print("Valid values for exchange includes 0 for OSE and 1 for Axess.")
        exit        
    tickers = scrape(url,"mbox",column=1, row=1, postspec_row = 1)
    removal1 = "OBX"
    removal2 = "OBTEST"
    for i in range(4):
        for ticker in tickers:
            if removal1 in ticker:
                tickers.remove(ticker)
            if removal2 in ticker:
                tickers.remove(ticker)
    return (tickers)

    
def get_company_names(exchange = 0):
    """Please specify 'exchange = 1' to receive Axess-tickers. Function returns OSE names by default."""
    if exchange == 0:
        url = "http://www.netfonds.no/quotes/kurs.php"
    elif exchange == 1:
        url = "http://www.netfonds.no/quotes/kurs.php?exchange=OAX"
    else:
        print("Valid values for exchange includes 0 for OSE and 1 for Axess.")
        exit 
    names = scrape(url, "mbox", row = 1, column = 0, postspec_row = 1)
    i = 0
    for x in names:
        if x == "DNB OBX":
            del names[i]
        for n in range(5):
            if x == "Oslo Børs Test":
                del names[i]
        i += 1
    return (names)

    
#SCRAPE FUNCTIONS 
#   :1 1
def _scrapec1_1(url, table_class, row = 0, column = 0):    
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[:row]:
        result = row.findAll('td')[column].text
        var.append(result)
    return(var)
#   :1 :1
def _scrapec1_c1(url, table_class, row = 0, column = 0):    
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[:row]:
        result = row.findAll('td')[:column].text
        var.append(result)
    return(var)
#   :1 1:
def _scrapec1_1c(url, table_class, row = 0, column = 0):    
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[:row]:
        result = row.findAll('td')[column:].text
        var.append(result)
    return(var)            
#   1: 1
def _scrape1c_1(url, table_class, row = 0, column = 0):    
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[row:]:
        result = row.findAll('td')[column].text
        var.append(result)
    return(var)
#1: :1
def _scrape1c_c1(url, table_class, row = 0, column = 0):    
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[row:]:
        result = row.findAll('td')[:column].text
        var.append(result)
    return(var)
#   1: 1:
def _scrape1c_1c(url, table_class, row = 0, column = 0):
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[row:]:
        result = row.findAll('td')[column:].text
        var.append(result)
    return(var)
#   1 :1
def _scrape1_c1(url, table_class, row = 0, column = 0):
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[row]:
        result = row.findAll('td')[:column].text
        var.append(result)
    return(var)
#   1 1
def _scrape1_1(url, table_class, row = 0, column = 0):
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[row]:
        result = row.findAll('td')[column].text
        var.append(result)
    return(var)
#1 1:
def _scrape1_1c(url, table_class, row = 0, column = 0):    
    var = []
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': table_class})
    for row in table.findAll('tr')[row]:
        result = row.findAll('td')[column:].text
        var.append(result)
    return(var)           
      
#Main Scrape Function
def scrape(url, table_class, row = 0, column = 0, prespec_row = 0, prespec_column = 0, postspec_row = 0, postspec_column = 0):
    """Scrape function requires several inputs to work.
        First input is the relevant URL from which to scrape data.
        Next, the function requires one to specify the class of the table to be scraped.
        Next, specify row & columns from which to start or end.
        Finally, you may write, e.g., "1:" by specifying a postspec_row/column,
        and ":1" by specifying a prespec_row/column - you do this by setting the desired
        specification = 1 """
    # :1 1
    if prespec_row == 1:
        # :1 :1
        if prespec_column == 1:
            return _scrapec1_c1(url, table_class, row, column)
        # :1 1:
        elif postspec_column == 1:
            return _scrapec1_1c(url, table_class, row, column)
        # :1 1
        else:
            return _scrapec1_1(url, table_class, row, column)
    # 1: 1
    elif postspec_row == 1:
        # 1: :1
        if prespec_column == 1:
            return _scrape1c_c1(url, table_class, row, column)
        # 1: 1:
        elif postspec_column == 1:
            return _scrape1c_1c(url, table_class, row, column)
        # 1: 1
        else:
            return _scrape1c_1(url, table_class, row, column)
    elif prespec_row == 0:
        # 1 :1
        if prespec_column == 1:
            return _scrape1_c1(url, table_class, row, column)
        # 1 1:
        elif postspec_column == 1:
            return _scrape1_1c(url, table_class, row, column)
        # 1 1
        else:
            return _scrape1_1(url, table_class, row, column)
    

def _price_sup(url, entry):
        resp = requests.get(url)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'id': "updatetable1"})
        result = table.findAll('td')[entry].text
        return result
        
def price(tickers, exchange = 0):
    """The function requires one or several tickers in list format. Please specify 'exchange = 1' to receive Axess-tickers. Function returns OSE tickers by default."""
    if exchange == 0:
        a = "http://www.netfonds.no/quotes/ppaper.php?paper="
        b = ".OSE"
    if exchange == 1:
        a = "http://www.netfonds.no/quotes/ppaper.php?paper="
        b = ".OAX"
    else:
        print("Valid values for exchange includes 0 for OSE and 1 for Axess.")
        exit
    prices = []
    for ticker in tickers:
        url = a+ticker+b
        appended = False
        i = 2
        while not appended:
            if _price_sup(url, i)[-1] == "%":    
                prices.append(_price_sup(url, i-2))
                print(ticker+"'s current price is: ",_price_sup(url, i-2))
                appended = True
            else:
                i+=1
    return(prices)


def daily_returns(tickers, exchange = 0):
    """The function requires one or several tickers in list format. Please specify 'exchange = 1' to receive Axess-tickers. Function returns OSE tickers by default."""
    if exchange == 0:
        a = "http://www.netfonds.no/quotes/ppaper.php?paper="
        b = ".OSE"
    if exchange == 1:
        a = "http://www.netfonds.no/quotes/ppaper.php?paper="
        b = ".OAX"
    else:
        print("Valid values for exchange includes 0 for OSE and 1 for Axess.")
        exit
    returns = []
    for ticker in tickers:
        url = a+ticker+b
        appended = False
        i = 2
        while not appended:
            if _price_sup(url, i)[-1] == "%":    
                returns.append(_price_sup(url, i))
                print(ticker,"'s daily return is: ",_price_sup(url, i))
                appended = True
            else:
                i+=1
    return(returns)


def complete_data(exchange = 0):
    """Please specify 'exchange = 1' to receive Axess-tickers. Function returns OSE tickers by default.
    The complete data-function returns tickers, market caps, daily return data, price data, and complete names of companies.
    Beware that the collection of said data may take a few minutes."""
    if exchange != 0 and exchange != 1:
        print("Error: Valid exchange choices include 0 for OSE and 1 for Axess.")
        exit
    print("\n This may take several minutes.")
    tickers = get_tickers(exchange = exchange)
    mcaps = mcap(tickers, exchange = exchange)
    returns = daily_returns(tickers, exchange = exchange)
    prices = price(tickers, exchange = exchange)
    names = get_company_names(exchange = exchange)
    return([tickers, names, prices, returns, mcaps])



