import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import plotly.express as px

print(glob.glob(r'D:\DATA ANALYST PROJECT\PROJECT 2\TIME_SERIES_PROJECT_S&P_500_STOCK_MARKET_CASE_STUDY\DATA\individual_stocks_5yr/*csv'))

print(len(glob.glob(r'D:\DATA ANALYST PROJECT\PROJECT 2\TIME_SERIES_PROJECT_S&P_500_STOCK_MARKET_CASE_STUDY\DATA\individual_stocks_5yr/*csv'))) ## total files we have 



# lets store files of those stock that we have to consider for analysis ..

company_list = [
    r'D:\DATA ANALYST PROJECT\PROJECT 2\TIME_SERIES_PROJECT_S&P_500_STOCK_MARKET_CASE_STUDY\DATA\individual_stocks_5yr\AAPL_data.csv' , 
    r'D:\DATA ANALYST PROJECT\PROJECT 2\TIME_SERIES_PROJECT_S&P_500_STOCK_MARKET_CASE_STUDY\DATA\individual_stocks_5yr\AMZN_data.csv' , 
    r'D:\DATA ANALYST PROJECT\PROJECT 2\TIME_SERIES_PROJECT_S&P_500_STOCK_MARKET_CASE_STUDY\DATA\individual_stocks_5yr\GOOG_data.csv' , 
    r'D:\DATA ANALYST PROJECT\PROJECT 2\TIME_SERIES_PROJECT_S&P_500_STOCK_MARKET_CASE_STUDY\DATA\individual_stocks_5yr\MSFT_data.csv'
    
]

## use Warnings package to get rid of any future warning ..

import warnings
from warnings import filterwarnings
filterwarnings('ignore')

all_data = pd.DataFrame()

for file in company_list:
    
    current_df = pd.read_csv(file)
    
    all_data = pd.concat([all_data, current_df], ignore_index=True)
    ##full_df = pd.concat([full_df , current_df] , ignore_index=True)
    
print(all_data.shape) ## dimensions of all_data dataframe ..)

print(all_data.head(6))

print(all_data['Name'].unique())



## Analysing change in price of the stock overtime !

print(all_data.isnull().sum()) ## checking missing values 
print(all_data.dtypes) ## checking data-types)

all_data['date'] = pd.to_datetime(all_data['date']) ## converting data-type of "date" featuer into date-time ..
print(all_data)
print(all_data.dtypes)

tech_list = all_data['Name'].unique()
print(tech_list)

plt.figure(figsize=(20,12))

for index , company in enumerate(tech_list , 1):
    plt.subplot(2 , 2 , index) ## creating subplot for each stock
    filter1 = all_data['Name']==company
    df = all_data[filter1]
    plt.plot(df['date'] , df['close']) ## plotting "date" vs "close"
    plt.title(company)
plt.show()



## moving average of the various stocks !

print(all_data.head(15))
print(all_data['close'].rolling(window=10).mean().head(14))

new_data = all_data.copy()

#### now lets consider different windows of rolling ,ie 10 days ,20 days ,30 days 
ma_day = [10 ,20 , 50]

for ma in ma_day:
    new_data['close_'+str(ma)] = new_data['close'].rolling(ma).mean()
    
print(new_data.tail(7))

new_data.set_index('date' , inplace=True)
print(new_data)

print(new_data.columns)

plt.figure(figsize=(20,12))

for index, company in enumerate(tech_list, 1):
    plt.subplot(2, 2, index)
    filter1 = new_data['Name'] == company
    df = new_data[filter1]
    df[['close_10', 'close_20', 'close_50']].plot(ax=plt.gca())
    plt.title(company)
    plt.xlabel('')  # Optional: hide x-label if too cluttered

plt.tight_layout()            # Auto-adjusts spacing to prevent overlap
plt.subplots_adjust(top=0.92)  # Optional: make room for suptitle if needed
plt.suptitle("Moving Averages of Tech Stocks (10, 20, 50 Days)", fontsize=18)
plt.show()


## analyse Closing price change in apple stock !
##### Daily Stock Return Formula

print(company_list)
apple = pd.read_csv(r'D:\DATA ANALYST PROJECT\PROJECT 2\TIME_SERIES_PROJECT_S&P_500_STOCK_MARKET_CASE_STUDY\DATA\individual_stocks_5yr\AAPL_data.csv')
print(apple.head(4))
print(apple['close'])
apple['Daily return(in %)'] = apple['close'].pct_change() * 100

### pct_change() returns : Percentage change between the current and a prior element.
print(apple.head(4))

px.line(apple , x="date" , y="Daily return(in %)") ## Plotting Line-plot of "date" vs "Daily return(in %)"..




## Performing resampling analysis of closing price ..
    
   ## a..yearly('Y')  , 
   ## b..quarterly('Q')   ,
   ## c..monthly('M') ,
   ## d..weekly basis ('W'), 
   ## e..Daily_basis('D')  
   ## f..minutes ('3T') , 
   ## g..30 second bins('30S')   ,
   ## h..resample('17min')
   
print(apple.dtypes)
apple['date'] =pd.to_datetime(apple['date'])
print(apple.dtypes)
print(apple.head(4))
apple.set_index('date' , inplace=True)
print(apple.head(4))
apple['close'].resample('M').mean() ## resample data on monthly basis ..

apple['close'].resample('M').mean().plot()
plt.title("Monthly Average Closing Price of Apple Stock")
plt.xlabel("Date")
plt.ylabel("Average Closing Price")
plt.grid(True)  # Optional: adds gridlines for clarity
plt.show()

apple['close'].resample('Y').mean() ## resample data on Yearly basis ..

apple['close'].resample('Y').mean().plot()

plt.title("Yearly Average Closing Price of Apple Stock", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Average Closing Price")
plt.grid(True)  # Optional: adds background grid
plt.tight_layout()
plt.show()

apple['close'].resample('Q').mean() ## resample data on Quarterly basis ..

apple['close'].resample('Q').mean().plot()

plt.title("Quarterly Average Closing Price of Apple Stock", fontsize=14)
plt.xlabel("Quarter")
plt.ylabel("Average Closing Price")
plt.grid(True)  # Optional but helpful for reading trends
plt.tight_layout()
plt.show()


## Whether closing prices of these tech companies (Amazon,Apple,Google,Microsoft) are correlated or not !

print(company_list)
print(company_list)
app = pd.read_csv(company_list[0])
amzn = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
msft = pd.read_csv(company_list[3])
closing_price = pd.DataFrame()

closing_price['apple_close'] = app['close']
closing_price['amzn_close'] = amzn['close']
closing_price['goog_close'] = google['close']
closing_price['msft_close'] = msft['close']
print(closing_price)

sns.pairplot(closing_price)
plt.suptitle("Pairwise Relationships of Stock Closing Prices", y=1.02, fontsize=16)
plt.show()

print(closing_price.corr())

##### co-relation plot for stock prices

plt.figure(figsize=(10, 8))  # Adjust size if needed
sns.heatmap(closing_price.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

plt.title("Correlation Heatmap of Stock Closing Prices", fontsize=16)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

## 7.. analyse Whether Daily change in Closing price of stocks or Daily Returns in Stock are co-related or not !

print(closing_price)
print(closing_price['apple_close'])
print(closing_price['apple_close'].shift(1))
print((closing_price['apple_close'] - closing_price['apple_close'].shift(1))/closing_price['apple_close'].shift(1) * 100)

for col in closing_price.columns:
    closing_price[col + '_pct_change'] = (closing_price[col] - closing_price[col].shift(1))/closing_price[col].shift(1) * 100
    
print(closing_price)
print(closing_price.columns)

clsing_p = closing_price[['apple_close_pct_change', 'amzn_close_pct_change',
       'goog_close_pct_change', 'msft_close_pct_change']]
print(clsing_p)

g = sns.PairGrid(data= clsing_p)
g.fig.suptitle("PairGrid: Stock Closing Price Relationships", fontsize=16)
g.map_diag(sns.histplot)
g.map_lower(sns.scatterplot)
g.map_upper(sns.kdeplot, cmap="Blues")
plt.show()


