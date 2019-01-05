
                          # Stochastic Simulation of Gene Expression
                          # Bokeh Dashboard developed by Stan Szydlo
                                   # January 4th, 2019
            
#.............................................................................................

import numpy as np
import pandas as pd
import random as rd

from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, Panel, ColumnDataSource
from bokeh.layouts import column, row, WidgetBox
from bokeh.models.widgets import Slider, Button, Tabs, Div
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

#.............................................................................................
    
# Stochastic Simulation Algorithm     
def runSSA(S_m = .005, # mRNA synthesis rate
           S_p = 0.1, # Protein synthesis rate
           D_m = .001, # mRNA degradation rate
           D_p = .0001, # Protein degradation rate 
           tMax = 1000, # simulation length in arbitrary time units
           D = 1, # initial DNA count
           M = 0, # initial mRNA count
           P = 0): # initial protein count

    # Initialization
    sim_data = pd.DataFrame(columns=['Time', 'mRNA', 'Protein'])
    t = 0 
    M_evo = [M]
    P_evo = [P]
    t_evo = [t]

    while t <= tMax: 
        # Define reaction propensities as functions of reaction rate and molecule count
        a1 = S_m*D
        a2 = S_p*M
        a3 = D_m*M
        a4 = D_p*P
        a_o = a1 + a2 + a3 + a4

        # pick random numbers from the uniform distributiom spanning [0,1]
        s1,s2 = np.random.random_sample(2)
        
        # When will the next reaction occur? 
        dt = -np.log(s1) / a_o
        
        # take a time step of size dt 
        t = t + dt
        t_evo.append(t)

       # Which reaction will occur next?
        if s2 < a1/a_o:
            M +=1 # mRNA synthesis 
            M_evo.append(M)
            P_evo.append(P)

        elif s2 < (a1+a2)/a_o:
            P +=1 # Protein synthesis 
            M_evo.append(M)
            P_evo.append(P)

        elif s2 < (a1+a2+a3)/a_o:
            M = M - 1 # mRNA degradation 
            M_evo.append(M)
            P_evo.append(P)

        else: 
            P = P - 1 # Protein degradation 
            M_evo.append(M)
            P_evo.append(P)
    
    # Merge columns 
    sim_data['Time'] = t_evo
    sim_data['mRNA'] = M_evo
    sim_data['Protein'] = P_evo

    # output RNA and Protein count over time
    return ColumnDataSource(sim_data)

#.............................................................................................

def style(p):
    
    # Title 
    p.title.align = 'center'
    p.title.text_font_size = '18pt'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '12pt'
    p.yaxis.axis_label_text_font_size = '12pt'

    # Tick labels
    p.xaxis.major_label_text_font_size = '10pt'
    p.yaxis.major_label_text_font_size = '10pt'

    return p

#.............................................................................................

def makePlot1(source):

    # Create a blank figure with labels
    p = figure(plot_width = 800, plot_height = 300, 
               title = "Stochastic Gene Expression",
               y_axis_label = 'Protein Count')

    # Add line glyph
    p.line('Time', 'Protein', source = source, color = 'limegreen')

    h = HoverTool(tooltips = [('(Time, Protein)', '($x, $y)')])
    p.add_tools(h)

    p = style(p)

    return(p) 

def makePlot2(source):

    # Create a blank figure with labels
    p = figure(plot_width = 800, plot_height = 300,
               x_axis_label = 'Time', 
               y_axis_label = 'mRNA Count')

    # Add line glyph
    p.line('Time', 'mRNA', source = source, color = 'limegreen')
    
    h = HoverTool(tooltips = [('(Time, Protein)', '($x, $y)')])
    p.add_tools(h)

    p = style(p)

    return(p) 

#.............................................................................................

# Generates new simulated data with fixed paramaters
def update_data():

    new_src = runSSA(tMax = tMax_select.value,
                    S_m = Sm_select.value,
                    S_p = Sp_select.value,
                    D_m = Dm_select.value,
                    D_p = Dp_select.value,
                    D = D_select.value,
                    M = M_select.value,
                    P = P_select.value)

    src.data.update(new_src.data)
 
    
# Generates new simulated data with updated paramaters
def update_param(attr, old, new):

    new_src = runSSA(tMax = tMax_select.value,
                    S_m = Sm_select.value,
                    S_p = Sp_select.value,
                    D_m = Dm_select.value,
                    D_p = Dp_select.value,
                    D = D_select.value,
                    M = M_select.value,
                    P = P_select.value)

    src.data.update(new_src.data)


#.............................................................................................

# Button to genrate new simulated data 
resimulate = Button(label = "RESIMULATE", button_type = "success")
resimulate.on_click(update_data)

# text instruction for adjusting slider
text = Div(text = "<i>Click along slider to modify parameter.</i>")

# Simulation length slider
tMax_select = Slider(start = 0, end = 2*(10**5), step = 10**3, value = 5*(10**4), 
                     title = 'Simulation Length')
tMax_select.on_change('value', update_param)

# RNA synthesis rate slider
Sm_select = Slider(start = 0, end = .02, step = .005, value = .01, 
                   title = 'mRNA Synthesis Rate')
Sm_select.on_change('value', update_param)

# Protein synthesis rate slider
Sp_select = Slider(start = 0, end = 1, step = .1, value = 0.1,
                   title = 'Protein Synthesis Rate')
Sp_select.on_change('value', update_param)

# RNA degradation rate slider
Dm_select = Slider(start = 0, end = .01, step = .001, value = .002,
                   title = 'mRNA Degradation Rate')
Dm_select.on_change('value', update_param)

# Protein degradation rate slider
Dp_select = Slider(start = 0, end = 0.001, step = .0001, value = .0001,
                   title = 'Protein Degradation Rate')
Dp_select.on_change('value', update_param)

# initial DNA count slider
D_select = Slider(start = 0, end = 10, step = 1, value = 1, 
                  title = 'Initial DNA')
D_select.on_change('value', update_param)

# initial RNA count slider
M_select = Slider(start = 0, end = 100, step = 1, value = 0, 
                  title = 'Initial mRNA')
M_select.on_change('value', update_param)

# Initial protein count control
P_select = Slider(start = 0, end = 1000, step = 1, value = 0, 
                  title = 'Initial Protein')
P_select.on_change('value', update_param)

#.............................................................................................

# Generate simulated data 
src = runSSA(tMax = tMax_select.value,
             S_m = Sm_select.value,
             S_p = Sp_select.value,
             D_m = Dm_select.value,
             D_p = Dp_select.value,
             D = D_select.value,
             M = M_select.value,
             P = P_select.value)

# Generate plots
p1 = makePlot1(src)
p2 = makePlot2(src)

# Put controls in a single element
controls = WidgetBox(resimulate,
                     text,
                     tMax_select,
                     Sm_select,
                     Sp_select,
                     Dm_select,
                     Dp_select,
                     D_select,
                     M_select,
                     P_select)

# Arrange the plots and controls
layout = row(controls, column(p1,p2))

# display dashboard
curdoc().add_root(layout)

    