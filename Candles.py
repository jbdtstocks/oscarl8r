from imports import *


def MarketData(ticker):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	closing_prices = df['close'].tolist()
	dates = df.index.tolist()
	fig = Figure()
	a = fig.subplot(421)
	a.plot(dates, closing_prices)

def StochasticOscillator(ticker):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	df['L14'] = df['low'].rolling(window=14).min()
	df['H14'] = df['high'].rolling(window=14).max()
	df['%K'] = 100*((df['close'].iloc[-1] - df['L14']) / (df['H14'] - df['L14']))
	df['%D'] = df['%K'].rolling(window=3).mean()
	(df[['%K', '%D']]).plot()
	plt.show()

def RelativeStrengthIndex(ticker):
	df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
	close = df['close']
	delta = close.diff()
	delta = delta[1:]
	up, down = delta.copy(), delta.copy()
	up[up < 0] = 0
	down[down > 0] = 0
	roll_up = up.ewm(span).mean()
	roll_down = (down.abs()).ewm(self.span).mean()
	RS1 = roll_up / roll_down
	RSI = 100.0 - (100.0 / (1.0 + RS1))
	seventy_perc = 70
	thirty_perc = 30
	RSI.plot()
	plt.axhline(y=70, color='r')
	plt.axhline(y=30, color='g')
	plt.show()

def StockStatistics(ticker):
	pass

def FullAnalysis(span=4):
	path = "C:/Users/david/oscarl8r/workingtickers.xlsx"
	tickers = pd.read_excel(path)
	tickers = tickers['TICKER'].tolist()
	for ticker in tickers:
		df = pdr.DataReader(ticker, 'iex', start='1/1/2018')
		closing_prices = df['close'].tolist()
		dates = df.index.tolist()
		# (df['close']).plot()
		df['L14'] = df['low'].rolling(window=14).min()
		df['H14'] = df['high'].rolling(window=14).max()
		df['%K'] = 100*((df['close'].iloc[-1] - df['L14']) / (df['H14'] - df['L14']))
		df['%D'] = df['%K'].rolling(window=3).mean()
		D = df['%D'].tolist()
		K = df['%K'].tolist()
		# (df[['%K', '%D']]).plot()
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
		seventy_perc = 70
		thirty_perc = 30
		# RSI.plot()
		# plt.axhline(y=70, color='r')
		# plt.axhline(y=30, color='g')
		df['70%'] = 70
		df['30%'] = 30
		df[['%K', '%D', 'close', 'RSI', '30%', '70%']].plot()
		plt.title(ticker)
		plt.show()
