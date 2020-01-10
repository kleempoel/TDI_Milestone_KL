from flask import Flask, render_template, request, redirect
import pandas as pd

from bokeh.embed import components
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("data/iris.data", 
    names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()


# Create the main plot
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


#Index page
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/Quandl_Tesla')
def Quandl_TSLA():
  return render_template('Quandl_TSLA.html')
  
@app.route('/notebook_embed')
def notebook_embed():
  return render_template('notebook_embed.html')

@app.route('/bokeh_add_plot_no_server')
def bokeh_add_plot_no_server():
  return render_template('bokeh_add_plot_no_server.html')

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

if __name__ == '__main__':
  app.run(port=5000)
