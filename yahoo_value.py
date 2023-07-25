import requests
import re #regex, not just a typo haha

sp500 = ['MMM','AOS','ABT','ABBV','ABMD','ACN','ATVI','ADM','ADBE','ADP','AAP','AES','AFL','A','AIG','APD','AKAM','ALK','ALB','ARE','ALGN','ALLE','LNT','ALL','GOOGL','GOOG','MO','AMZN','AMCR'\
         ,'AMD','AEE','AAL','AEP','AXP','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','APA','AAPL','AMAT','APTV','ANET','AIZ','T','ATO','ADSK','AZO','AVB','AVY','BKR'\
         ,'BLL','BAC','BBWI','BAX','BDX','WRB','BRK','BBY','BIO','TECH','BIIB','BLK','BK','BA','BKNG','BWA','BXP','BSX','BMY','AVGO','BR','BRO','BF','CHRW','CDNS','CZR','CPT','CPB','COF','CAH'\
         ,'KMX','CCL','CARR','CTLT','CAT','CBOE','CBRE','CDW','CE','CNC','CNP','CDAY','CERN','CF','CRL','SCHW','CHTR','CVX','CMG','CB','CHD','CI','CINF','CTAS','CSCO','C','CFG','CTXS','CLX'\
         ,'CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','COP','ED','STZ','CEG','COO','CPRT','GLW','CTVA','COST','CTRA','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY'\
         ,'DVN','DXCM','FANG','DLR','DFS','DISH','DIS','DG','DLTR','D','DPZ','DOV','DOW','DTE','DUK','DRE','DD','DXC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ENPH','ETR','EOG','EPAM'\
         ,'EFX','EQIX','EQR','ESS','EL','ETSY','RE','EVRG','ES','EXC','EXPE','EXPD','EXR','XOM','FFIV','FDS','FAST','FRT','FDX','FITB','FRC','FE','FIS','FISV','FLT','FMC','F','FTNT','FTV'\
         ,'FBHS','FOXA','FOX','BEN','FCX','AJG','GRMN','IT','GE','GNRC','GD','GIS','GPC','GILD','GL','GPN','GM','GS','GWW','HAL','HIG','HAS','HCA','PEAK','HSIC','HSY','HES','HPE','HLT','HOLX'\
         ,'HD','HON','HRL','HST','HWM','HPQ','HUM','HII','HBAN','IEX','IDXX','ITW','ILMN','INCY','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JBHT','JKHY'\
         ,'J','JNJ','JCI','JPM','JNPR','K','KEY','KEYS','KMB','KIM','KMI','KLAC','KHC','KR','LHX','LH','LRCX','LW','LVS','LDOS','LEN','LLY','LNC','LIN','LYV','LKQ','LMT','L','LOW','LUMN'\
         ,'LYB','MTB','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MTCH','MKC','MCD','MCK','MDT','MRK','FB','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MRNA','MHK','MOH','TAP','MDLZ'\
         ,'MPWR','MNST','MCO','MS','MOS','MSI','MSCI','NDAQ','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NDSN','NSC','NTRS','NOC','NLOK','NCLH','NRG','NUE','NVDA','NVR'\
         ,'NXPI','ORLY','OXY','ODFL','OMC','OKE','ORCL','OGN','OTIS','PCAR','PKG','PARA','PH','PAYX','PAYC','PYPL','PENN','PNR','PEP','PKI','PFE','PM','PSX','PNW','PXD','PNC','POOL','PPG'\
         ,'PPL','PFG','PG','PGR','PLD','PRU','PEG','PTC','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RL','RJF','RTX','O','REG','REGN','RF','RSG','RMD','RHI','ROK','ROL','ROP','ROST','RCL'\
         ,'SPGI','CRM','SBAC','SLB','STX','SEE','SRE','NOW','SHW','SBNY','SPG','SWKS','SJM','SNA','SEDG','SO','LUV','SWK','SBUX','STT','STE','SYK','SIVB','SYF','SNPS','SYY','TMUS','TROW'\
         ,'TTWO','TPR','TGT','TEL','TDY','TFX','TER','TSLA','TXN','TXT','TMO','TJX','TSCO','TT','TDG','TRV','TRMB','TFC','TWTR','TYL','TSN','USB','UDR','ULTA','UAA','UA','UNP','UAL','UNH'\
         ,'UPS','URI','UHS','VLO','VTR','VRSN','VRSK','VZ','VRTX','VFC','VTRS','V','VNO','VMC','WAB','WMT','WBA','WBD','WM','WAT','WEC','WFC','WELL','WST','WDC','WRK','WY','WHR','WMB','WTW'\
         ,'WYNN','XEL','XYL','YUM','ZBRA','ZBH','ZION','ZTS']

tickers = sp500
number_pattern = "[0123456789.]+"
price_pattern = '<fin-streamer class="Fw\(b\) Fz\(36px\) Mb\(-4px\) D\(ib\)" data-symbol="[A-Z]{1,5}" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="'
value_pattern = '<div class="Fw\(b\) Fl\(end\)--m Fz\(s\) C\(\$primaryColor">' #regex format (pattern)
value_text = '<div class="Fw(b) Fl(end)--m Fz(s) C($primaryColor">' #bare html search format (text)
maintenance_pattern = 'Our engineers are working quickly to resolve the issue.'
maintenance_text = 'Our engineers are working quickly to resolve the issue.'

def yahoo_url(ticker):
    return "https://finance.yahoo.com/quote/" + ticker +"?p=" + ticker + "&.tsrc=fin-srch"

def parse_value(r):
    try:
        location = r.text.index(value_text)+len(value_text)
    except ValueError:
        if r.text.find(maintenance_text) == -1:
            return ("Website Error", -3)
        return ("Unfound", -2)
    value = r.text[location:location+20]
    if value.startswith("Overvalued"):
        return ("Overvalued", 2)
    if value.startswith("Near Fair Value"):
        return ("Near Fair Value", 1)
    if value.startswith("Undervalued"):
        return ("Undervalued", 0)
    return ("Other", -1)

def parse_price(r):
    try:
        location = re.search(price_pattern, r.text).end()
    except AttributeError:
        if r.text.find(maintenance_text) == -1:
            return -3
        return -2
    try:
        price = eval(re.match(number_pattern, r.text[location:]).group(0))
        return price
    except TypeError:
        return -1

def info_dict(): #very lengthy operation, needs to download html from 500 websites, about half a gigabyte
    values = {}
    for ticker in tickers:
        url = yahoo_url(ticker)
        r = requests.get(url)
        value = parse_value(r)
        price = parse_price(r)
        values[ticker] = {}
        values[ticker]['value'] = value[1] #extracts value id, we don't need text
        values[ticker]['price'] = price #isn't a tuple
    return values

def main():
    for ticker in tickers:#like valuedict but for testing
        url = yahoo_url(ticker)
        r = requests.get(url)
        value = parse_value(r)
        price = parse_price(r)
        print(ticker,price,value)

if __name__ == "__main__":
    main()
