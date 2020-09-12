import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quandl
from matplotlib import style
import datetime

style.use('fivethirtyeight')

api_key = "odP3fjxY1Nqk-s6yKfmt"

data = quandl.get("NSE/PNB", start_date="2017-12-31",
                  end_date="2020-09-01", paginate=True, api_key=api_key)
# print(data)
data['15d'] = np.round(data['Close'].rolling(window=15).mean(), 2)
data['60d'] = np.round(data['Close'].rolling(window=60).mean(), 2)

data[['Close', '15d', '60d']].plot(grid=True, figsize=(10, 8))
# plt.show()
data['15d-60d'] = data['15d']-data['60d']

data['Stance'] = np.where(data['15d-60d'] > 60, 1, 0)
data['Stance'] = np.where(data['15d-60d'] < 60, -1, data['Stance'])

# print(data['Stance'].value_counts())
data['Stance'].value_counts()
data['Stance'].plot(lw=2, ylim=[-1.1, 1.1])
# plt.show()

data['Stock Returns'] = np.log(data['Close']/data['Close'].shift(1))
data['SMAC Strategy'] = data['Stock Returns']*data['Stance'].shift(1)
data[['Stock Returns', 'SMAC Strategy']].plot(grid=True, figsize=(10, 6))

plt.show()
