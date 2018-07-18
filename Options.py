from imports import *

def Forecast(ticker, type = 'market', api='iex', start='1/1/2015', end=None):
	"""
	-------------
	Function that forecasts the price of a stock over a period of time.
	Uses the fbprophet class Prophet() to forecast

	Args:
		ticker - symbol for stock
		type - market is default
		api - API to pull stock data from...default is IEX
		start - start date for data...default is 1/1/2015
		end - end date for data...default is None
	Returns:
		Forecast - Pandas dataframe object
		Plot of forecast/raw data
	-------------
	"""

	df = pdr.DataReader(ticker, api, start, end)
	new = pd.DataFrame()
	if api == 'quandl':
		open = 'AdjOpen'
		close = 'AdjClose'
		high = 'AdjHigh'
		low = 'AdjLow'
		volume = 'AdjVolume'
	if api == 'iex':
		open = 'open'
		close = 'close'
		high = 'high'
		low = 'low'
		volume = 'volume'
	if type == 'market':
		new = new.append(df[close])
		new = new.T
		new['ds'] = new.index
		new['y'] = new[close]
		cols = new.columns.tolist()
		cols.remove(close)
		new = new[cols]
	if type == 'RSI':
		rsi = RelativeStrengthIndex(ticker)
		rsi.columns = ['RSI']
		if isinstance(rsi, pd.DataFrame):
			print(rsi)
		new = new.append(rsi)
		print(new)
		new['ds'] = new.index
		new['y'] = new['RSI']
		cols = new.columns.tolist()
		print(cols)
		cols.remove('RSI')
		new = new[cols]
		print(rsi)
	if type == 'Stochastic':
		pass
	m = Prophet(changepoint_prior_scale=.1999)
	m.fit(new)
	future = m.make_future_dataframe(periods=7)
	forecast = m.predict(future)
	print("Yesterday's closing price:", df[close][-1])
	print("Prediction:", '\n', forecast[['ds', 'trend','yhat_lower', 'yhat_upper']])
	forecast['avg'] = (forecast['yhat_upper'] +forecast['yhat_lower']) / 2
	avg = forecast[['ds', 'avg']]
	print(avg)
	forecast.to_excel(ticker + '__' + '7DayForecast.xlsx')
	m.plot(forecast)
	plt.title(ticker)
	plt.show(block=False)
	# m.plot_components(forecast)
	return forecast

def OptionsProfitCalculator(exp_price, strike_price, option_price):
	'''
	------------
	Calculates the profit of buying an option

	Args:
		exp_price = expected price of stock
		strike_price = strike price
		option_price = price per share for option
	Returns:
		profit = profit in dollars
	-------------
	'''

	profit = (((exp_price - strike_price)*100) / (option_price*100))
	print("Net options profit:", '$' + profit)
	return profit

Forecast()
OptionsProfitCalculator()
