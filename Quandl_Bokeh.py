# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:08:46 2020

@author: leempoel
"""

#getting data from quandl
import os
os.chdir("C:\Data\The Data Incubator\TDI_Milestone_KL")
import quandl
import pandas as pd
quandl.ApiConfig.api_key = 'G8fYyzS1iQS44dkAFC2x'
#data=quandl.get('GDT/BUT_PI', start_date='2011-01-08', end_date='2020-01-08')

#make list of dates
import datetime
#base = datetime.date.today()-datetime.timedelta(days=375) #going back 2 months because the data is not available for this year
#numdays = 30
#date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
##get data for that list of dates
#for x in range(numdays):
#    newdate = date_list[x].strftime("%Y-%m-%d")
#    data=quandl.get_table('SHARADAR/SEP', date=newdate, ticker='TSLA')
#    print(newdate)
#    print(data['close'])
#
#    
#datetime.isoformat(date_list)
#datetime.strptime(date_list[2], "%d/%m/%y")
#date_list.strftime("%d/%m/%y")
#data=quandl.get_table('SHARADAR/SEP', date=newdate, ticker='TSLA')
#data=quandl.get_table('SHARADAR/SEP', date='2018-11-04', ticker='TSLA')
#
#data=quandl.get_table('SHARADAR/SEP', date='2018-12-31,2018-11-30', ticker='TSLA')
#data2=quandl.get_table('SHARADAR/SEP', date='2018-11-30', ticker='TSLA')
data=quandl.get("BATS/BATS_TSLA", start_date='2019-12-08', end_date='2020-01-08')
pdata=pd.DataFrame(data=data)
#pdata2=pdata[['Close']] 
#pdata2["Date"]=pdata.index


#plotting the data in html
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import DatetimeTickFormatter

p = figure(plot_width=600, plot_height=400, title="Tesla stock volume from Quandl")
p.line(pdata.index, pdata["Total Volume"], line_width=2)
p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.major_label_orientation = 3.14/4
p.yaxis.axis_label = "Total Volume"

html = file_html(p, CDN, "Quandl TSLA stocks")
Html_file= open("templates/Quandl_TSLA.html","w")
Html_file.write(html)
Html_file.close()
#
#import os
#os.getcwd()