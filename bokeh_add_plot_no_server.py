from bokeh.io import show, output_file, curstate
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

output_file('bokeh_add_plot_no_server.html')
curstate().file['resources'].js_components.append('bokeh-api')
show(main_row)