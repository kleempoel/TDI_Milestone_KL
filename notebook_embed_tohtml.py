import yaml

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.themes import Theme

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature



def modify_doc(doc):
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25),
                  y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """))



from bokeh.resources import CDN
from bokeh.embed import file_html
t=modify_doc
html = file_html(modify_doc, CDN, "bokey_seasurface")
Html_file= open("templates/bokey_seasurface.html","w")
Html_file.write(html)
Html_file.close()

#show(modify_doc) # notebook_url="http://localhost:8888" 



from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import Button, CustomJS
from bokeh.layouts import column

f1 = figure()
f1.x(x=[1, 2, 3], y=[3, 2, 1])
main_row = column(f1)

b = Button(label='Add plot',
           callback=CustomJS(args=dict(main_row=main_row),
                             code="""
    f = Bokeh.Plotting.figure();
    f.cross({x: [1, 2, 3], y: [3, 2, 1]});
    main_row.children.push(f);
    main_row.properties.children.change.emit();
"""))

main_row.children.append(b)

output_file('templates/bokeh_add_plot_no_server.html')
#curstate().file['resources'].js_components.append('bokeh-api')
show(main_row)





