from imports import *

root = Tk ()

class Stocks:
	def __init__(self, root):
		self.ticker = 'ticker'
		self.stock_entry = Entry(root)
		self.stock_entry.grid(column=0, row=1, sticky='nw')
		self.span = 4
		
	def MarketData(self):
		df = pdr.DataReader(self.ticker, 'iex', start='1/1/2018')
		df['close'].plot()
		plt.show()

	def StochasticOscillator(self):
		df = pdr.DataReader(self.ticker, 'iex', start='1/1/2018')
		df['L14'] = df['low'].rolling(window=14).min()
		df['H14'] = df['high'].rolling(window=14).max()
		df['%K'] = 100*((df['close'].iloc[-1] - df['L14']) / (df['H14'] - df['L14']))
		df['%D'] = df['%K'].rolling(window=3).mean()
		df[['%K', '%D']].plot()
		plt.show()

	def RelativeStrengthIndex(self):
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

	def StockStatistics(self):
		pass

gui = Stocks(root)
root.mainloop()
