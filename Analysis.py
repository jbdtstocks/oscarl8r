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
	x_ = df.index.tolist()

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
	ax.axes.set_xticklabels(x_)
	fig.autofmt_xdate()
	plt.title(ticker)
	ax.axes.set_ylim(bottom=0)
	plt.show()

def average_directional_movement_index(df, n, n_ADX):
	"""
	Calculate the Average Directional Movement Index for given data.
	:param df: pandas.DataFrame
	:param n:
	:param n_ADX:
	:return: pandas.DataFrame
	"""
	n = 14
	n_ADX = 14
	i = 0
	UpI = []
	DoI = []
	while i + 1 <= df.index[-1]:
		UpMove = df.loc[i + 1, 'High'] - df.loc[i, 'High']
		DoMove = df.loc[i, 'Low'] - df.loc[i + 1, 'Low']
		if UpMove > DoMove and UpMove > 0:
			UpD = UpMove
		else:
			UpD = 0
		UpI.append(UpD)
		if DoMove > UpMove and DoMove > 0:
			DoD = DoMove
		else:
			DoD = 0
		DoI.append(DoD)
		i = i + 1
	i = 0
	TR_l = [0]
	while i < df.index[-1]:
		TR = max(df.loc[i + 1, 'High'], df.loc[i, 'Close']) - min(df.loc[i + 1, 'Low'], df.loc[i, 'Close'])
		TR_l.append(TR)
		i = i + 1
	TR_s = pd.Series(TR_l)
	ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean())
	UpI = pd.Series(UpI)
	DoI = pd.Series(DoI)
	PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean() / ATR)
	NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean() / ATR)
	ADX = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n_ADX, min_periods=n_ADX).mean(),
			name='ADX_' + str(n) + '_' + str(n_ADX))
	df = df.join(ADX)
	return df

def Screener():
	xl = pd.read_excel('top_100_stocks.xlsx')
	tickers = xl['TICKER'].tolist()
	tickers = sorted(tickers)
	for ticker in tickers:
		try:
			df = pdr.DataReader(ticker, 'iex', start='1/1/2015')
			df['SMA14'] = df['close'].rolling(window=14).mean()
			df['SMA28'] = df['close'].rolling(window=28).mean()
			df['SMA100'] = df['close'].rolling(window=100).mean()
			df['EMA 14'] = df['close'].ewm(span=20, adjust=False).mean()
			df['EMA 28'] = df['close'].ewm(span=50, adjust=False).mean()
			df['MACD'] = df['close'].ewm(span=12, adjust=False).mean() - df['close'].ewm(span=26, adjust=False).mean()
			df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
			df = df.dropna()
			sma14 = df['SMA14'].tolist()
			sma28 = df['SMA28'].tolist()
			ema14 = df['EMA 14'].tolist()
			ema28 = df['EMA 28'].tolist()
			macd = df['MACD'].tolist()
			signal = df['Signal'].tolist()
			close = df['close'].tolist()
			buy_sell = []
			buy_sell2 = []
			up_down = []
			for i,j in zip(close,sma14):
				if i > j and j:
					buy_sell.append('buy')
				if j > i and j:
					buy_sell.append('sell')
			for i,j in zip(sma14, sma28):
				if i > j:
					buy_sell2.append('buy')
				else:
					buy_sell2.append('sell')
			for i,j in zip(macd, signal):
				if i > j:
					up_down.append('UP')
				if j > i:
					up_down.append("DOWN")
			df['Buy/Sell'] = buy_sell
			df['SMA Buy/Sell'] = buy_sell2
			df["UP/DOWN"] = up_down
			if buy_sell2[-1] == 'buy' and up_down[-1] == 'UP':
				print(ticker, df['close'].iloc[-1], 'CALL')
			if buy_sell2[-1] == 'sell' and up_down[-1] == 'DOWN':
				print(ticker, df['close'].iloc[-1], 'PUT')
			# print(ticker,df.tail())
		except:
			pass
	# # df.to_excel('StrongTrendList.xlsx')
	# fromaddr = "jbdtstocks@gmail.com"
	# toaddr = "jbdtstocks@gmail.com"
	# msg = MIMEMultipart()
	# msg['From'] = fromaddr
	# msg['To'] = toaddr
	# msg['Subject'] = "Stock Screener"
	# body = "Daily stock screen"
	# msg.attach(MIMEText(body, 'plain'))
	# filename = "StrongTrendList.xlsx"
	# attachment = open("StrongTrendList.xlsx", "rb")
	# p = MIMEBase('application', 'octet-stream')
	# p.set_payload((attachment).read())
	# encoders.encode_base64(p)
	# p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	# msg.attach(p)
	# s = smtplib.SMTP('smtp.gmail.com', 587)
	# s.starttls()
	# s.login(fromaddr, "Stocker#1")
	# text = msg.as_string()
	# s.sendmail(fromaddr, toaddr, text)
	# s.quit()
#########################################################################
# StochasticOscillator('LB')
# FullAnalysis('LMT')
# Forecast()
# print(RelativeStrengthIndex('AAPL'))
Screener()
