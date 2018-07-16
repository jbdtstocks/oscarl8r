from imports import *

def MarketData(ticker):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	price = df['close'].iloc[-1]
	df['close'].plot()
	plt.title(ticker)
	plt.show()

def StochasticOscillator(ticker):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	df['L14'] = df['low'].rolling(window=14).min()
	df['H14'] = df['high'].rolling(window=14).max()
	df['%K'] = 100*((df['close'].iloc[-1] - df['L14']) / (df['H14'] - df['L14']))
	df['%D'] = df['%K'].rolling(window=3).mean()
	if (0):
		(df[['%K', '%D']]).plot()
		plt.show()
	if (1):
		pass
	return df['%K'], df['%D']

def RelativeStrengthIndex(ticker, span=4):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	rsi_df = pd.DataFrame()
	close = df['close']
	delta = close.diff()
	delta = delta[1:]
	up, down = delta.copy(), delta.copy()
	up[up < 0] = 0
	down[down > 0] = 0
	roll_up = up.ewm(span).mean()
	roll_down = (down.abs()).ewm(span).mean()
	RS1 = roll_up / roll_down
	RSI = 100.0 - (100.0 / (1.0 + RS1))
	if (0):
		df['RSI'].plot()
		plt.axhline(y=70, color='r')
		plt.axhline(y=30, color='g')
		plt.show()
	if (1):
		pass
	rsi_df = rsi_df.append(RSI)
	rsi_df = rsi_df.T
	return rsi_df

def StockStatistics(ticker):
	pass

def Forecast(ticker, type = 'market', api='iex', start='1/1/2018', end=None):
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
	m = Prophet(changepoint_prior_scale=1.2)
	m.fit(new)
	future = m.make_future_dataframe(periods=180)
	forecast = m.predict(future)
	m.plot(forecast)
	plt.title(ticker)
	plt.show()
	# m.plot_components(forecast)

def FullAnalysis(ticker, api='iex', span=4):
	path = "C:/Users/david/oscarl8r/workingtickers.xlsx"
	tickers = pd.read_excel(path)
	tickers = tickers['TICKER'].tolist()
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
	for ticker in tickers:
		df = pdr.DataReader(ticker, api, start='1/1/2018')
		df['L14'] = df[low].rolling(window=14).min()
		df['H14'] = df[high].rolling(window=14).max()
		df['%K'] = 100*((df[close].iloc[-1] - df['L14']) / (df['H14'] - df['L14']))
		df['%D'] = df['%K'].rolling(window=3).mean()
		close = df['close']
		delta = close.diff()
		delta = delta[1:]
		up, down = delta.copy(), delta.copy()
		up[up < 0] = 0
		down[down > 0] = 0
		roll_up = up.ewm(span).mean()
		roll_down = (down.abs()).ewm(span).mean()
		RS1 = roll_up / roll_down
		df['RSI'] = 100.0 - (100.0 / (1.0 + RS1))
		df['70%'] = 70
		df['30%'] = 30
		df[['%K', '%D', close, 'RSI', '30%', '70%']].plot()
		# df['close'].plot()
		plt.title(ticker)
		plt.show()

def FilterByPrice(api='robinhood', start='1/1/2018'):
	path = "C:/Users/david/oscarl8r/workingtickers.xlsx"
	tickers = pd.read_excel(path)
	tickers = tickers['TICKER'].tolist()
	filter_list = []
	for ticker in tickers:
		try:
			df = pdr.DataReader(ticker, api, start)
			print("Loaded:", ticker)
			price = df['close_price'].iloc[-1]
			print(float(price))
			if float(price) <= 60 and float(price) > 2:
				filter_list.append(ticker)
		except:
			print("Failed:",ticker, price)
			pass
	filter_df = pd.DataFrame({'Filter Price': filter_list})
	filter_df.to_csv('price_filtered_tickers.csv')

# MarketData('AAPL')
# FullAnalysis('AAPL')
# Forecast('AAPL')
# print(RelativeStrengthIndex('AAPL'))
FilterByPrice()
