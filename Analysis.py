from imports import *

def MarketData(ticker):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	price = df['close'].iloc[-1]
	print("Average closing price:", df['close'].mean())
	df['close'].plot()
	plt.title(ticker)
	plt.show()

def StochasticOscillator(ticker):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	df['L14'] = df['low'].rolling(window=14).min()
	df['H14'] = df['high'].rolling(window=14).max()
	df['%K'] = 100*((df['close'].iloc[-1] - df['L14']) / (df['H14'] - df['L14']))
	df['%D'] = df['%K'].rolling(window=3).mean()
	if (1):
		(df[['%K', '%D']]).plot()
		plt.show()
	if (0):
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
	if (1):
		RSI.plot()
		plt.axhline(y=70, color='r')
		plt.axhline(y=30, color='g')
		plt.show()
	if (0):
		pass
	rsi_df = rsi_df.append(RSI)
	rsi_df = rsi_df.T
	return rsi_df

def Forecast(type = 'market', api='iex', start='4/1/2018', end=None):
	optionlist = [
					'AAPL', 'ADBE', 'AMZN', 'BA', 'COST', 'DIS', 'FB', 'GOOG',
					'IBM', 'MSFT', 'NFLX', 'NKE', 'SQ', 'TGT', 'TSLA', 'V'
	]
	writer = ExcelWriter('OptionsForecast.xlsx')
	for ticker in optionlist:
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
		m = Prophet(changepoint_prior_scale=.17)
		m.fit(new)
		future = m.make_future_dataframe(periods=3)
		forecast = m.predict(future)
		past_week = forecast
		forecast['Predict. Avg.'] = (forecast['yhat_lower'] + forecast['yhat_upper']) / 2
		last_day = forecast.iloc[-1]
		next_to_last_day = forecast.iloc[-2]
		forecast['Combined Avg.'] = (last_day['Predict. Avg.'] + next_to_last_day['Predict. Avg.']) / 2
		filtered_data = forecast[['ds', 'trend', 'yhat_lower', 'yhat_upper', 'Predict. Avg.', 'Combined Avg.']]
		filtered_data = filtered_data[-7:]
		filtered_data.to_excel(writer, ticker)
		# m.plot(forecast)
		# plt.title(ticker)
		# plt.show(block=False)
	writer.save()

def FullAnalysis(ticker, api='iex', span=4):
	path = "C:/Users/david/oscarl8r/workingtickers.xlsx"
	tickers = pd.read_excel(path)
	tickers = tickers['TICKER'].tolist()

	fig, ax = plt.subplots()
	years = YearLocator()
	months = MonthLocator()
	days = DayLocator()
	yrsformatter = DateFormatter('%Y')
	mnthsformatter = DateFormatter('%M')
	dayformatter = DateFormatter('%D')

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

	# for ticker in tickers:
	df = pdr.DataReader(ticker, api, start='1/1/2018')
	df['L14'] = df[low].rolling(window=14).min()
	df['H14'] = df[high].rolling(window=14).max()
	df['%K'] = 100*((df[close].iloc[-1] - df['L14']) / (df['H14'] - df['L14']))
	df['%D'] = df['%K'].rolling(window=3).mean()
	closing = df[close]
	delta = closing.diff()
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
	new_df = df[['%K', '%D', close, 'RSI', '30%', '70%']]

	K = df['%K'].values
	D = df['%D'].values
	RSI = df['RSI'].values
	thirty = df['30%'].values
	seventy = df['70%'].values
	x_ = df.index.astype(str)
	print(x_)

	plt.plot(x_, K, label='%K')
	plt.plot(x_, D, label='%D')
	plt.plot(x_, RSI, label='RSI')
	plt.plot(x_, thirty, label='30%')
	plt.plot(x_, seventy, label='70%')
	plt.plot(x_, closing, label='Close')

	plt.legend(loc=2)
	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(mnthsformatter)
	ax.xaxis.set_minor_locator(days)
	fig.autofmt_xdate()
	plt.title(ticker)
	ax.axes.set_ylim(bottom=0)
	plt.show()
#########################################################################
# StochasticOscillator('ARNC')
FullAnalysis('ARNC')
# Forecast()
# print(RelativeStrengthIndex('AAPL'))
