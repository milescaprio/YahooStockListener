A short program which attempts to trade stocks. Not effective nor should be used for actual trading, just a fun day project.

A script accesses the internet to look at Yahoo Finance, and each stock there in the S&P 500. It retrieves the HTML and parses
it to find how Yahoo thinks the stock is priced currently (Overvalued, Near Fair Value, Undervalued), and then uses this information
and stores it to decide on stocks to buy and sell.

A virtual portfolio is made and artificially maintained. You can then run exchange_now to buy/sell stocks at the current moment using
this data, and then do so again later.

Not polished.

Last modified June 2022