# followed this demo
# https://www.youtube.com/watch?v=0e-lsstqCdY&list=PLQVvvaa0QuDcOdF96TBtRtuQksErCEBYZ&index=1
#By Lindsay Gillespie 1/5/21
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as m_dates
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
from yahoo_fin.stock_info import *

style.use('ggplot')
print("Do you want to use graph data or create new data?")
opt = int(input("Please Enter 1 for Graph Data or Enter 2 for open and close or Enter 3 for detailed info or 0 to quit "))
while (opt != 0):
    if (opt == 1):
        # The data already exists
        symbol = input("Please enter the symbol of the company you want to look up or ^GSPC for S&P 500 ")
        symbol = symbol.lower()
        tablename = symbol + ".csv"
        try:
            df = pd.read_csv(tablename, parse_dates=True, index_col=0)
            df["Adj Close"].plot()
            plt.show()
        except:
            print("There is no table for that Symbol")

    if (opt == 2):
        sy = input("Please enter the symbol of the company you want to look up or ^GSPC for S&P 500 ")
        symbol = sy.split(",")
        # symbol=symbol.upper()
        startY = int(input("Please enter starting year "))
        startM = int(input("Please enter starting month "))
        startD = int(input("Please enter starting day "))
        endY = int(input("Please enter ending year "))
        endM = int(input("Please enter ending month "))
        endD = int(input("Please enter ending day "))
        try:
            start = dt.datetime(startY, startM, startD)
            end = dt.datetime(endY, endM, endD)
            master = pd.DataFrame()
            yf.pdr_override()
            aList = []
            for ticker in symbol:
                # getting data
                df = web.get_data_yahoo(ticker, start, end, 'd')
                # calculating 200 ma
                df['200ma'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
                df["Symbol"] = ticker
                aList.append(df)
            master = pd.concat(aList)
            tablename = sy.lower() + ".csv"
            master.to_csv(tablename)
        except:
            print("Something went wrong please try again")
    if (opt == 3):
        sy = input("Please enter the symbol of the company you want to look up or ^GSPC for S&P 500 ")
        symbol = sy.split(",")
        try:
            master = pd.DataFrame()
            aList = []
            for ticker in symbol:
                # pulling other info
                dataDF = pd.DataFrame()
                financial = get_financials(ticker, yearly=True, quarterly=False)
                # i want data from the yearly income statement
                yearlyIncome = financial['yearly_income_statement']
                #To add new column copy and paste and existing column then rename the green text then the nuber at the end change to the approraite row number
                #to find the row number type print(financial)

                #this section is the grouping called yearly income
                # net income  row 4
                dataDF['netIncome'] = yearlyIncome.iloc[4]
                # operating income row 8
                dataDF['operatingIncome'] = yearlyIncome.iloc[8]
                # operating expense which is in row 9
                dataDF['otherOperatingExpenses'] = yearlyIncome.iloc[9]
                # income tax expense row 14
                dataDF['incomeTaxExpense'] = yearlyIncome.iloc[14]
                # total revenue row 15
                dataDF['totalRevenue'] = yearlyIncome.iloc[15]
                # total operating expense 16
                dataDF['totaloperatingExpense'] = yearlyIncome.iloc[16]

                # this section is the grouping called yearly balnce sheet
                yearlyBalanceSheet = financial['yearly_balance_sheet']
                # cash row 14
                dataDF['cash'] = yearlyBalanceSheet.iloc[14]
                # total libailties row 15
                dataDF['totalCurrentLibilites'] = yearlyBalanceSheet.iloc[15]
                # long term investments row 21
                dataDF['long term investments'] = yearlyBalanceSheet.iloc[21]

                # this section is the grouping called yearly cah flow
                yearlyCashFlow = financial['yearly_cash_flow']
                # dividends paid
                dataDF['DivdendsPaid'] = yearlyCashFlow.iloc[14]

            # merging each indivdual dataframe into a single dataframe
                aList.append(dataDF)
            master = pd.concat(aList)
            tablename = sy.lower() + ".csv"
            master.to_csv(tablename)
            print("COMPLETE")
        except:
            print("Something went wrong please try again")
    if(opt==4):
        sy = input("Please enter the symbol of the company you want to look up or ^GSPC for S&P 500 ")
        symbol = sy.split(",")
        try:
            master = pd.DataFrame()
            aList = []
            for ticker in symbol:
                dataDF = pd.DataFrame()
                stats = get_stats(ticker)
                # add any new columns you find the row number and change the last number in the statement
                # payout ratio row 23
                dataDF['payout ratio'] = stats.iloc[23]
                #Beta row 0
                dataDF['Beta'] = stats.iloc[0]
                #52 week change row
                dataDF['52 week change'] = stats.iloc[1]
                #200 day moving avg
                dataDF['200 day moving avg'] = stats.iloc[6]
                #forward dividend yeild
                dataDF['forward dividend yeild'] = stats.iloc[19]
                #trailing dividend yeild
                dataDF['trailing dividend yeild'] = stats.iloc[21]
                #5 year avg dividend yeild
                dataDF['5 year avg dividend yeild'] = stats.iloc[22]
                #dividend date
                dataDF['dividend date'] = stats.iloc[24]
                #ex- dividen date
                dataDF['EX dividend date'] = stats.iloc[25]
                #return on equity
                dataDF['return on equity'] = stats.iloc[33]
                #Revenue (ttm)
                dataDF['Revenue (ttm)'] = stats.iloc[34]
                aList.append(dataDF)
            master = pd.concat(aList)
            tablename = sy.lower() + ".csv"
            master.to_csv(tablename)
            print("COMPLETE")
        except:
            print("Something went wrong please try again")
    print("Do you want to use graph data or create new data?")
    opt = int(input("Please Enter 1 for Graph Data or Enter 2 for open and close or Enter 3 for detailed info or 0 to quit "))
