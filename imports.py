import os
import time
from time import sleep
import datetime as dt
import glob as gl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
import pandas as pd
from pandas import ExcelWriter
import pandas_datareader as pdr
from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.dates import (MONTHLY, DateFormatter, rrulewrapper, RRuleLocator, YearLocator, MonthLocator, DayLocator)
import plotly
plotly.tools.set_credentials_file(username='jbdtstocks', api_key='cCqpKMsmASdpYw5a5Hgc')
import plotly.plotly as py
import plotly.graph_objs as go
from fbprophet import Prophet
import sklearn as sk
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import *
from sklearn.linear_model import *
from sklearn.svm import *
from sklearn.metrics import *
from sklearn.grid_search import *
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import ImageTk, Image
print("Imports successful")
