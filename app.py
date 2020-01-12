from flask import Flask, render_template, request, redirect
import pandas as pd

from bokeh.embed import components
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.models import DatetimeTickFormatter
import quandl
quandl.ApiConfig.api_key = 'G8fYyzS1iQS44dkAFC2x'

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("data/iris.data", 
    names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()

#Load stock data
stock_current_feature_names=list(['TSLA','GOOG','INT','AMD'])
import datetime
today= datetime.date.today().strftime("%Y-%m-%d")
inidate=(datetime.date.today()-datetime.timedelta(days=365)).strftime("%Y-%m-%d")
TSLA=pd.DataFrame(data=quandl.get("BATS/BATS_TSLA", start_date=inidate, end_date=today))
GOOG=pd.DataFrame(data=quandl.get("BATS/BATS_GOOG", start_date=inidate, end_date=today))
INT=pd.DataFrame(data=quandl.get("BATS/BATS_INT", start_date=inidate, end_date=today))
AMD=pd.DataFrame(data=quandl.get("BATS/BATS_AMD", start_date=inidate, end_date=today))

# Create the main plot for iris
def create_figure(current_feature_name, bins):
    bins=bins
    bins_val=pd.qcut(iris_df[current_feature_name], q=bins,precision=1).value_counts()
    bins_count=list(bins_val)
    inter_iris= [str(x) for x in range(1,bins + 1)]
    source = ColumnDataSource(data=dict(intervals=inter_iris, counts=bins_count))
    p = figure(x_range=inter_iris, plot_height=350, toolbar_location=None, title="Counts")
    p.vbar(x='intervals', top='counts', width=0.9, source=source,
           line_color='white', fill_color=factor_cmap('intervals', palette=Spectral6, factors=inter_iris))
    
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = round(max(bins_count)*1.1,0)
    return p

# Create the main plot for stock
def create_figure_stock(stock_current_feature_name):
    if stock_current_feature_name=='TSLA':
        data_stock=TSLA
    elif stock_current_feature_name=='GOOG':
        data_stock=GOOG
    elif stock_current_feature_name=='INT':
        data_stock=INT
    elif stock_current_feature_name=='AMD':
        data_stock=AMD
    p = figure(plot_width=600, plot_height=400, toolbar_location=None, 
               title=stock_current_feature_name + " stock volume from Quandl (" + inidate + " - " + today + ")")
    p.line(data_stock.index, data_stock["Total Volume"], line_width=2)
    p.xaxis.formatter=DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
    p.xaxis.major_label_orientation = 3.14/4
    p.yaxis.axis_label = "Total Volume"
    p.yaxis.formatter=NumeralTickFormatter(format="00")
    return p



#Index page
@app.route('/')
def index():
  return render_template('index.html')

#@app.route('/Quandl_Tesla')
#def Quandl_TSLA():
#  return render_template('Quandl_TSLA.html')

@app.route('/Quandl_Tesla_dyn')
def Quandl_TSLA():
    # Determine the selected feature
	stock_current_feature_name = request.args.get("feature_name")
	if stock_current_feature_name == None:
		stock_current_feature_name = "TSLA"

	# Create the plot
	plot = create_figure_stock(stock_current_feature_name)
		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("Quandl_TSLA_dyn.html", script=script, div=div,
		feature_names=stock_current_feature_names,  current_feature_name=stock_current_feature_name)
  
@app.route('/iris_index1')
def iris_interactive_bokeh():
    # Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	if current_feature_name == None:
		current_feature_name = "Sepal Length"

	# Create the plot
	plot = create_figure(current_feature_name, 8)
		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("iris_index1.html", script=script, div=div,
		feature_names=feature_names,  current_feature_name=current_feature_name)
    
@app.route('/notebook_embed')
def notebook_embed():
  return render_template('notebook_embed.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=5000)
