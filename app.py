from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/Quandl_TSLA')
def Quandl_TSLA():
  return render_template('Quandl_TSLA.html')
  
@app.route('/notebook_embed')
def notebook_embed():
  return render_template('notebook_embed.html')

@app.route('/bokeh_add_plot_no_server')
def bokeh_add_plot_no_server():
  return render_template('bokeh_add_plot_no_server.html')

if __name__ == '__main__':
  app.run(port=5000)
