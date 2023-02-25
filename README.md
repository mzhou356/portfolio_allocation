# portfolio_allocation
This is a personal program that calculates investment portfolio allocation. Below are the assets considered for the asset allocation:
* stocks
* bonds
* cash
* derivatives
* mortgage
* mutual funds
* ETFs
* other/not classified.

## Note:
* The configuration file and html file are not uploaded to github.
* statements are not uploaded to github either.
* The parsing code will need to be edited based upon your PDF statements.
* Due to the configuration file is not uploaded, I removed pytest from github action. The pytest won't pass because it would complain configuration module is not found. The code in tests folder would work if you include your own configuration file.
* The two main tools used for PDF statements are:
   1. [Py2PDF](https://pypi.org/project/py2pdf/)
   2. [tabula-py](https://pypi.org/project/tabula-py/)

 ## How it works:
 Assume you have the configuration file, you just need to run python3 main.py. It would ask you a few questions about static fund. It then fetches asset allocation for each mutual fund and ETF. Once all of the fund information is calculated, it would open your default browswer with 2 asset allocation tables displayed:
 1. asset allocation by asset type
 2. asset allocation by asset type and geographical location (split by international and US).

 You need to replace the statements in the statement folders monthly and quarterly. Rerun the program to get an updated allocation. This allows you to see if you are still following your asset allocation strategy and if portofolio rebalance is needed.

 A separate email alert project will trigger a monthly/quarterly alert to keep the asset allocation information up to date.
